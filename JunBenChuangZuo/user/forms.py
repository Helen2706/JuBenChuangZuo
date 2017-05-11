#coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField
from wtforms.validators import DataRequired,EqualTo,Email,Length,InputRequired,Regexp

class RegisterForm(FlaskForm):
    email = StringField('邮箱', validators=[InputRequired(), Email(),Length(min=4, max=25)])
    username = StringField('用户名', validators=[InputRequired(),Length(min=6, max=25),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'用户名必须只包含数字、字母、下划线！')])
    password = PasswordField('密码', validators=[InputRequired(), Length(min=6, max=25),EqualTo('password2', message='两次密码输入不一致！')])
    password2 = PasswordField('确认密码', validators=[InputRequired()])
    submit = SubmitField('注册')

class LoginForm(FlaskForm):
    email = StringField('邮箱',validators=[InputRequired(),Email(),Length(min=4, max=25)])
    password = PasswordField('密码',validators=[InputRequired(), Length(min=6, max=25)])
    submit = SubmitField('登录')