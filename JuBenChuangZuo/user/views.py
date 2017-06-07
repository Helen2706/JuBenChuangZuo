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
    if request.method == "GET":
        return render_template("user/login.html")
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user.verify_password(password):
            login_user(user, )
            return redirect(request.args.get('next') or url_for('main.home'))
        flash("用户名或密码错误！")
        return redirect(url_for('.login'))
@user.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'GET':
        strs = generate_verification_image_code()
        session['code_text'] = strs
        return render_template('user/register.html')
    else:
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        telephone = request.form.get("telephone")
        confirmcode = request.form.get("confirmcode")
        user = User(email, username, password, telephone)
        if(confirmcode==session['code_text']):
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email,'确认账户','user/email/email_body',user=user,token=token)
            login_user(user, True)
            return render_template("user/emailInfo.html")

@user.route('/validate/username',methods=['POST','GET'])
def validateusername():
    username = request.form.get('username')
    if User.query.filter_by(username=username).first():
        return jsonify(False)
    return jsonify(True)

#注册时检查邮箱是否存在
@user.route('/validate/email',methods=['POST','GET'])
def validateemail():
    email = request.form.get('email')
    if User.query.filter_by(email=email).first():
        return jsonify(False)
    return jsonify(True)

#登录检查邮箱是否已注册
@user.route('/loginvalidate/email',methods=['POST','GET'])
def validateemail2():
    email = request.form.get('email')
    if User.query.filter_by(email=email).first():
        return jsonify(True)
    return jsonify(False)

#检查验证码是否正确
@user.route('/validate/confirmcode',methods=['POST','GET'])
def validateconfirmcode():
    confirmcode = request.form.get('confirmcode')
    if confirmcode == session['code_text']:
        return jsonify(True)
    return jsonify(False)

#检查用户名密码是否正确
@user.route('/validate/password',methods=['POST','GET'])
def validatepassword():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()
    if user.verify_password(password):
        return jsonify(True)
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


