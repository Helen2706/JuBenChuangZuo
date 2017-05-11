#coding:utf8

from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3306/database'
    
    db.init_app(app)
    bootstrap.init_app(app)
    app.config['SECRET_KEY'] = '\xca\x0c\x86\x04\x98@\x02b\x1b7\x8c\x88]\x1b\xd7"+\xe6px@\xc3#\\'
    return app