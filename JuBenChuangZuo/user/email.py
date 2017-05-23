#coding:utf8
from threading import Thread
from models import mail
from flask import current_app,render_template
from flask_mail import Message

def send_async_mail(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to,subject,template,**kwargs):
    app = current_app._get_current_object()
    # sender：发送方，recipient邮件接收方列表
    msg = Message(app.config['MAIL_SUBJECT_PREFIX']+'-'+subject,sender="18763823073@163.com",recipients=[to])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    thr = Thread(target=send_async_mail,args=[app,msg])
    thr.start()
    return thr

