#coding:utf8

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField,ValidationError
from wtforms.validators import InputRequired,EqualTo,Email,Length,Regexp
from models import User

class LoginForm(FlaskForm):
    email = StringField('邮箱',validators=[InputRequired(),Email(),Length(min=6,max=20)])
    password = PasswordField('密码',validators=[InputRequired(),Length(min=6,max=20)])
    remember_me = BooleanField('记住我',default=False)
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    email = StringField('邮箱')
    username = StringField('用户名')
    password = PasswordField('密码')
    password2 = PasswordField('确认密码')
    verification_code = StringField('验证码')
    submit = SubmitField('注册')

    # email = StringField('邮箱', validators=[InputRequired(), Email(), Length(min=6, max=20)])
    # username = StringField('用户名', validators=[InputRequired(), Length(min=6, max=20),
    #                                           Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名必须以字母开头，只包含数字、字母、下划线！')])
    # password = PasswordField('密码', validators=[EqualTo('password2',message='两次输入密码不一致'),InputRequired(), Length(min=6, max=20)])
    # password2 = PasswordField('确认密码')
    # verification_code = StringField('验证码', validators=[InputRequired(), Length(4, 4, message='填写4位验证码')])
    # submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')



