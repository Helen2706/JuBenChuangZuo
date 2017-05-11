#coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField
from wtforms.validators import DataRequired,EqualTo,Email

class RegisterForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='两次密码输入不一致！')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

class LoginForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    submit = SubmitField('登录')