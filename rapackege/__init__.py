from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import config
app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret
#user +pymysql for ubuntu
app.config['SQLALCHEMY_DATABASE_URI'] = config.sqlconn

db = SQLAlchemy(app)
from rapackege import routes
from . import auth
app.register_blueprint(auth.bp)
