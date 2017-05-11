#coding=utf-8

from . import user
from flask import render_template
from .forms import LoginForm, RegisterForm
from models import User,db


@user.route('/',methods=['GET','POST'])
def login():
    email = None
    password = None
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user == None:
            return render_template('user/error.html', email=email)
        elif user.password != password:
            return render_template('user/error.html', email=email)
        else:
            return render_template('user/success.html',email=email)
    return render_template('user/login.html',form=form)

@user.route('/register',methods=['GET','POST'])
def register():
    email = None
    username = None
    password = None
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User(email,username,password)
        db.session.add(user)
        db.session.commit()
        return render_template('user/success.html', email=email)
    return render_template('user/register.html',form=form)
