import flask, flask.views
from flask import url_for, request, session, redirect, jsonify, Response
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
import json
import datetime
import time
import os


app = flask.Flask(__name__)
cors = CORS(app)
db = SQLAlchemy(app)
app.secret_key = '234234rfascasascqweqscasefsdvqwefe2323234dvsv'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
API_KEY = 'ecc67d28db284a2fb351d58fe18965f9'
# os.environ['DATABASE_URL']

now = datetime.datetime.now()
MORNING_START = now.replace(hour=8, minute=0, second=0, microsecond=0)
MORNING_END = now.replace(hour=12, minute=0, second=0, microsecond=0)

AFTERNOON_START = now.replace(hour=13, minute=0, second=0, microsecond=0)
AFTERNOON_END = now.replace(hour=16, minute=0, second=0, microsecond=0)


class Serializer(object):
  __public__ = None

  def to_serializable_dict(self):
    dict = {}
    for public_key in self.__public__:
      value = getattr(self, public_key)
      if value:
        dict[public_key] = value
    return dict


class SWEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Serializer):
      return obj.to_serializable_dict()
    if isinstance(obj, (datetime)):
      return obj.isoformat()
    return json.JSONEncoder.default(self, obj)


def SWJsonify(*args, **kwargs):
  return app.response_class(json.dumps(dict(*args, **kwargs), cls=SWEncoder, indent=None if request.is_xhr else 2), mimetype='application/json')
  # from https://github.com/mitsuhiko/flask/blob/master/flask/helpers.py


class Log(db.Model, Serializer):
    __public__ = ['id','date','id_no','name','section','time_in','time_out','timestamp']
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    id_no = db.Column(db.String(20))
    name = db.Column(db.String(60))
    level = db.Column(db.String(10))
    section = db.Column(db.String(30))
    time_in = db.Column(db.String(10))
    time_out = db.Column(db.String(10))
    timestamp = db.Column(db.String(50))


class Late(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    id_no = db.Column(db.String(20))
    time_in = db.Column(db.String(10))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    level = db.Column(db.String(10))
    section = db.Column(db.String(30))
    department = db.Column(db.String(20))

class IngAdmin(sqla.ModelView):
    column_display_pk = True
admin = Admin(app)
admin.add_view(IngAdmin(Student, db.session))
admin.add_view(IngAdmin(Late, db.session))


def get_hour(time):
    if time[6:8] == 'PM' and time[:2] != '12':
        hour = int(time[:2]) + 12
        print hour
        return hour
    hour = int(time[:2])
    print hour
    return hour



@app.route('/', methods=['GET', 'POST'])
def index():
    a = Log.query.filter_by().order_by(Log.timestamp.desc()).all()
    return SWJsonify({'Logs': a})


@app.route('/addlog', methods=['GET', 'POST'])
def add_log():
    api_key = flask.request.form.get('api_key')

    if not api_key or api_key != API_KEY:
        return 'Invalid API Key!'

    id_no = flask.request.form.get('id_no')
    name = flask.request.form.get('name')
    level = flask.request.form.get('level')
    section = flask.request.form.get('section')
    date = flask.request.form.get('date')
    time_in = flask.request.form.get('time_in')

    add_this = Log(
            date=date,
            id_no=id_no,
            name=name,
            level=level,
            section=section,
            time_in=time_in,
            time_out='None',
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
    
    db.session.add(add_this)
    db.session.commit()

    time_now = now.replace(hour=get_hour(time_in), minute=int(time_in[3:5]))

    if (time_now >= MORNING_START and time_now < MORNING_END) or (time_now > AFTERNOON_START and time_now < AFTERNOON_END):
        late = Late(date=date,id_no=id_no,time_in=time_in)
        db.session.add(late)
        db.session.commit()

    return SWJsonify({
        'Status': 'Logged In',
        'Log': Log.query.all()
        })


@app.route('/timeout', methods=['GET', 'POST'])
def time_out():
    api_key = flask.request.form.get('api_key')

    if not api_key or api_key != API_KEY:
        return 'Invalid API Key!'

    id_no = flask.request.form.get('id_no')
    time_out = flask.request.form.get('time_out')

    a = Log.query.filter_by(id_no=id_no).order_by(Log.timestamp.desc()).first()
    a.time_out=time_out  
    db.session.commit()

    return SWJsonify({'Status': 'Logged Out',
                      'Log': Log.query.filter_by(id_no=id_no)\
                      .order_by(Log.timestamp.desc()).first()
                      })


@app.route('/db/rebuild', methods=['GET', 'POST'])
def rebuild_database():
    db.drop_all()
    db.create_all()

    db.session.commit()

    return SWJsonify({'Status': 'Database Rebuild Success'})


if __name__ == '__main__':
    app.debug = True
    app.run(port=int(os.environ['PORT']), host='0.0.0.0')

    # port=int(os.environ['PORT']), host='0.0.0.0'