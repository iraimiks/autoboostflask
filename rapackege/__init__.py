from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import config
import locale
import glob
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret
#user +pymysql for ubuntu
app.config['SQLALCHEMY_DATABASE_URI'] = config.sqlconn
db = SQLAlchemy(app)


#app_lang = 'lv'
#locale.setlocale(locale.LC_ALL, app_lang)

language_list = glob.glob("**/loca/*.json")
languages = {}
for lang in language_list:
    filename = lang.split('\\')

    print("CHeck: ",filename)
    lang_code = filename[2].split('.')[0]
    print("CHeck: ",lang_code)
    with open(lang, 'r', encoding='utf8') as file:
        languages[lang_code] = json.loads(file.read())

from rapackege import routes
from . import auth
from . import dataedit
from . import orders
app.register_blueprint(auth.bp)
app.register_blueprint(dataedit.ed)
app.register_blueprint(orders.ord)

