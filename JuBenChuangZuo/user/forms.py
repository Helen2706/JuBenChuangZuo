#coding:utf8

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField
from wtforms.validators import InputRequired,EqualTo,Email,Length,Regexp

class LoginForm(FlaskForm):
    email = StringField('邮箱',validators=[InputRequired(),Email(),Length(min=6,max=20)])
    password = PasswordField('密码',validators=[InputRequired(),Length(min=6,max=20)])
    remember_me = BooleanField('记住我',default=False)
    submit = SubmitField('提交')

class RegisterForm(FlaskForm):
    email = StringField('邮箱', validators=[InputRequired(), Email(), Length(min=6, max=20)])
    username = StringField('用户名', validators=[InputRequired(), Length(min=6, max=20),
                                              Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名必须只包含数字、字母、下划线！')])
    password = PasswordField('密码', validators=[EqualTo('password2',message='两次输入密码不一致'),InputRequired(), Length(min=6, max=20)])
    password2 = PasswordField('确认密码')
    submit = SubmitField('注册')