#coding:utf8
from flask import flash,redirect,jsonify,url_for,render_template,request,session
from . import user
from forms import LoginForm,RegisterForm
from models import User,db
from email import send_email
from validate import generate_verification_image_code
from flask_login import login_user, logout_user, login_required, \
    current_user

@user.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('用户不存在！')
            return redirect(url_for('.login'))
        elif not user.verify_password(form.password.data):
            flash('用户名或密码错误！')
            return redirect(url_for('.login'))
        else:
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.home'))
    return render_template('user/login.html',form=form)

@user.route("/validate_code",methods=['POST','GET'])
def validate():
    userInput = request.form.get('params')
    if userInput == session['code_text']:
        return jsonify("True")
    return jsonify("False")

@user.route('/register',methods=['POST','GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        validate_code = form.verification_code.data
        print "输入："+validate_code
        print "session:"+session['code_text']
        if(validate_code==session['code_text']):
            user = User(email, username, password)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            # send_email(user.email,'确认账户','user/email/email_body',user=user,token=token)
            login_user(user, True)
            return render_template("user/emailInfo.html")
        flash("验证码错误，请重新输入")
        return render_template('user/register.html',form=form)
    strs = generate_verification_image_code()
    session['code_text'] = strs
    print strs
    print request.args.get('next')
    return render_template('user/register.html',form=form)

# 用户收到确认邮件后，点击链接的处理函数
@user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        flash('您已认证，无需再次认证')
        return render_template('user/confirmInfo.html')
    if current_user.confirm(token):
        flash('您的账号认证成功')
        return render_template('user/confirmInfo.html')
    else:
        flash('认证信息无效')
        message = "点击此处再次发送认证信息"
        return render_template('user/confirmInfo.html',message = message)
    return render_template('user/confirmInfo.html')

# 定义全局的请求钩子，当用户登录但未确认账户时，并且访问的是user蓝本之外的路由时，拦截请求
# @user.before_app_request
# def before_request():
#     if current_user.is_authenticated \
#         and not current_user.confirmed \
#         and request.endpoint[:5] != 'user.' \
#         and request.endpoint != 'static':
#         return redirect(url_for('user.unconfirmed'))

# 当请求钩子拦截到请求时，跳转到这个页面
@user.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous:
        flash("还未登录，请您登录")
        return redirect(url_for('user.login'))
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    return render_template('user/unconfirmed.html')

# 当用户需要重新发送确认邮件时执行
@user.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认账户', 'user/email/email_body', user=user, token=token)
    return render_template("user/emailInfo.html")

# 创建新的页面用于测试某些页面需要登录才能访问
@user.route('/test')
@login_required
def test_login():
    return render_template("user/test_login.html")

# 注销用户
@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已注销登录')
    return redirect(url_for('user.login'))




