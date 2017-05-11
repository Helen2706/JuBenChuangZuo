#coding:utf8

from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    bootstrap.init_app(app)
    return app