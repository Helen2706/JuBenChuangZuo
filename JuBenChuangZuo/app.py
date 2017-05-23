#!/usr/bin/env python
#coding:utf8

from flask import Flask, redirect, url_for
from models import db
from models import mail,login_manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:1234@localhost:3306/database'
app.config['SECRET_KEY'] = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
# 与发送邮件相关的配置
app.config.update(
    MAIL_SERVER='smtp.163.com',
    MAIL_PORT=25,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='18763823073@163.com', #邮件的用户名和密码可以在系统的环境变量中进行添加
    MAIL_PASSWORD='13467065634,lhl',
    MAIL_DEBUG=True,
    MAIL_SUBJECT_PREFIX="如艺影视大数据",
)

mail.init_app(app)
login_manager.init_app(app)
db.init_app(app)

from main import main as main_blueprint     # 蓝本类，调用实例对象，将网址分模块处理
app.register_blueprint(blueprint=main_blueprint, url_prefix='/')
from editor import editor as editor_blueprint
app.register_blueprint(blueprint=editor_blueprint, url_prefix='/<projectId>/editor')
from analysis import analysis as analysis_blueprint
app.register_blueprint(blueprint=analysis_blueprint, url_prefix='/<projectId>/analysis')
from user import user as user_blueprint
app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')

@app.route('/')
def index():
    return redirect(url_for('main.home'))

# 路由重定向，全部交给geteditor处理
@app.route('/<projectId>/')
def select_project(projectId):
    if not str(projectId).startswith('No'):
        return ''
    return redirect(url_for('editor.getEditor', projectId=projectId))

# 启动server服务器
if __name__ == '__main__':
    # app.run(debug = True)
    app.run(port=2000, debug = True)    # 显示调试信息