import flask, flask.views
from flask import url_for, request, session, redirect
from jinja2 import environment, FileSystemLoader
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import admin
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin import Admin, BaseView, expose
from flask import render_template, request
from flask import session, redirect
from flask_oauth import OAuth
from functools import wraps
import time
import os

app = flask.Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = '234234rfascasascqweqscasefsdvqwefe2323234dvsv'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# os.environ['DATABASE_URL']

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    id_no = db.Column(db.String(20))
    name = db.Column(db.String(60))
    level = db.Column(db.String(10))
    section = db.Column(db.String(30))
    time_in = db.Column(db.String(10))
    time_out = db.Column(db.String(10))


@app.route('/', methods=['GET', 'POST'])
def index():
    log = Log.query.all()
    return flask.render_template('index.html',date=time.strftime("%B %d, %Y"),log=log)


@app.route('/addlog', methods=['GET', 'POST'])
def add_log():
    id_no = flask.request.args.get('id_no')
    name = flask.request.args.get('name')
    level = flask.request.args.get('level')
    section = flask.request.args.get('section')
    date = flask.request.args.get('date')
    time_in = flask.request.args.get('time_in')

    add_this = Log(date=date, id_no=id_no, name=name,
            level=level, section=section, time_in=time_in)
    
    db.session.add(add_this)
    db.session.commit()

    return 'ok'


@app.route('/db/rebuild', methods=['GET', 'POST'])
def rebuild_database():
    db.drop_all()
    db.create_all()

    a = Log(date='March 10, 2015', id_no='2011334281', name='Barcelona, Jasper Oliver E',
            level='2nd Year', section='Fidelity', time_in='08:00 AM')

    db.session.add(a)
    db.session.commit()

    return 'ok'


if __name__ == '__main__':
    app.debug = True
    app.run(port=int(os.environ['PORT']), host='0.0.0.0')

    # port=int(os.environ['PORT']), host='0.0.0.0'