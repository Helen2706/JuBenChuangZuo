#coding:utf8
from flask import flash,redirect,url_for,render_template
from . import user
from forms import LoginForm,RegisterForm
from models import User,db

@user.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('用户不存在！')
            return redirect(url_for('.login'))
        elif user.password!=form.password.data:
            flash('用户名或密码错误！')
            return redirect(url_for('.login'))
        else:
            return redirect(url_for('main.home'))
    return render_template('user/login.html',form=form)
