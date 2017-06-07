#coding:utf8
from flask import flash,redirect,url_for,render_template,request,session,jsonify
from . import user
from forms import LoginForm,RegisterForm
from models import User,db
from email import send_email
from validate import generate_verification_image_code
from flask_login import login_user, logout_user, login_required, \
    current_user

@user.route('/', methods=['POST','GET'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if user is None:
    #         flash('用户不存在！')
    #         return redirect(url_for('.login'))
    #     elif not user.verify_password(form.password.data):
    #         flash('用户名或密码错误！')
    #         return redirect(url_for('.login'))
    #     else:
    #         login_user(user,form.remember_me.data)
    #         return redirect(request.args.get('next') or url_for('main.home'))
    return render_template('user/login.html',form=form)

@user.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'GET':
        strs = generate_verification_image_code()
        session['code_text'] = strs
        return render_template('user/register.html')
    else:
        username = request.form.get("username")
        print username
        return username

@user.route('/validate/username',methods=['POST','GET'])
def validateusername():
    return jsonify(False)

@user.route('/register/protocol')
def register_protocol():
    return render_template("user/register_protocol.html")

# 用户收到确认邮件后，点击链接的处理函数
@user.route('/confirm/<token>')
@login_required
def confirm(token):
    print current_user.confirmed
    if current_user.confirmed:
        flash('您已认证，无需再次认证')
        return render_template('user/confirmInfo.html')
    if current_user.confirm(token):
        flash('您的账号认证成功')
        return render_template('user/confirmInfo.html')
    else:
        flash('认证信息无效')
        return render_template('user/confirmInfo.html')
    return render_template('user/confirmInfo.html')


