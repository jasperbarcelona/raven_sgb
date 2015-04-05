import flask, flask.views
from flask import url_for, request, session, redirect, jsonify, Response, make_response, current_app
from jinja2 import environment, FileSystemLoader
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import admin
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin import Admin, BaseView, expose
from dateutil.parser import parse as parse_date
from flask import render_template, request
from functools import update_wrapper
from flask import session, redirect
from datetime import timedelta
from datetime import datetime
from functools import wraps
from threading import Timer
import datetime
import time
import json
import os


app = flask.Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = '234234rfascasascqweqscasefsdvqwefe2323234dvsv'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
API_KEY = 'ecc67d28db284a2fb351d58fe18965f9'
# os.environ['DATABASE_URL']

now = datetime.datetime.now()

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
  return app.response_class(json.dumps(dict(*args, **kwargs), cls=SWEncoder, 
         indent=None if request.is_xhr else 2), mimetype='application/json')
        # from https://github.com/mitsuhiko/flask/blob/master/flask/helpers.py

class School(db.Model, Serializer):
    __public__= ['id','api_key','password','id_no','name','address','city','email','tel']

    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(32))
    password = db.Column(db.String(20))
    name = db.Column(db.String(50))
    address = db.Column(db.String(120))
    city = db.Column(db.String(30))
    email = db.Column(db.String(60))
    tel = db.Column(db.String(15))
    faculty_morning_start = db.Column(db.String(30))
    faculty_morning_end = db.Column(db.String(30))
    faculty_afternoon_start = db.Column(db.String(30))
    faculty_afternoon_end = db.Column(db.String(30))
    student_morning_start = db.Column(db.String(30))
    student_morning_end = db.Column(db.String(30))
    student_afternoon_start = db.Column(db.String(30))
    student_afternoon_end = db.Column(db.String(30))


class Log(db.Model, Serializer):
    __public__ = ['id','school_id','date','id_no','name','level',
                  'department','section','time_in','time_out','timestamp']

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer)
    date = db.Column(db.String(20))
    id_no = db.Column(db.String(20))
    name = db.Column(db.String(60))
    level = db.Column(db.String(10))
    section = db.Column(db.String(30))
    department = db.Column(db.String(30))
    time_in = db.Column(db.String(10))
    military_time = db.Column(db.DateTime)
    time_out = db.Column(db.String(10))
    timestamp = db.Column(db.String(50))


class Student(db.Model):
    __public__ = ['id','school_id','id_no','first_name','last_name','middle_name',
                  'level','department','section','parent_contact']

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer)
    id_no = db.Column(db.String(20))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    middle_name = db.Column(db.String(30))
    level = db.Column(db.String(30))
    department = db.Column(db.String(30))
    section = db.Column(db.String(30))
    absences = db.Column(db.String(3))
    lates = db.Column(db.String(3))
    parent_contact = db.Column(db.String(12))


class Absent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer)
    id_no = db.Column(db.String(20))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    middle_name = db.Column(db.String(30))
    level = db.Column(db.String(30))
    department = db.Column(db.String(30))
    section = db.Column(db.String(30))
    date = db.Column(db.String(20))


class IngAdmin(sqla.ModelView):
    column_display_pk = True
admin = Admin(app)
admin.add_view(IngAdmin(School, db.session))
admin.add_view(IngAdmin(Log, db.session))
admin.add_view(IngAdmin(Student, db.session))


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


def get_hour(time):
    if time[6:8] == 'PM' and time[:2] != '12':
        hour = int(time[:2]) + 12
        print hour
        return hour
    hour = int(time[:2])
    print hour
    return hour


def authenticate_user(school_id, password):
    if not School.query.filter_by(id=school_id, password=password).first():
        return False
    return True


def mark_absent():
    print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    print 'its working'
    start_timer()


def start_timer():
    x=datetime.datetime.now()
    y=x.replace( hour=1, minute=4, second=0, microsecond=0)
    delta_t=y-x
    secs=delta_t.seconds+1
    t = Timer(secs, mark_absent)
    t.start()
    print 'time until mark_absent: ' + str(secs/60) + 'mins'


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session:
        return redirect('/loginpage')
    start_timer()
    return flask.render_template('index.html', view=session['department'])


@app.route('/data', methods=['GET', 'POST'])
def load_data():
    school = School.query.filter_by(api_key=session['api_key']).first()
    print 'xxxxxxxx'
    print school.name
    logs = Log.query.filter_by(
        school_id=session['school_id'],
        department=session['department']
        ).order_by(Log.timestamp.desc()).all()

    l = Log.query.filter(
        str(Log.military_time)[11:]>=str(parse_date(school.student_afternoon_start))[11:],
        str(Log.military_time)[11:]<=str(parse_date(school.student_afternoon_end))[11:],
        Log.school_id==session['school_id'],
        Log.department==session['department']
        ).order_by(Log.timestamp.desc()).all()

    attendance = Student.query.filter_by(
        department=session['department'])\
        .order_by(Student.last_name).all()

    return flask.render_template(
        'tables.html',
        log=logs,
        late=l,
        attendance=attendance, 
        view=session['department']
        )


@app.route('/view', methods=['GET', 'POST'])
def change_view():
    view = flask.request.form.get('view')
    session['department'] = view
    return redirect('/data')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session:
        return redirect('/')
    
    school_id = flask.request.form.get('school_id')
    password = flask.request.form.get('password')

    if not authenticate_user(school_id, password):
        return redirect('/loginpage')

    session['school_id'] = school_id
    session['api_key'] = School.query.filter_by(id=school_id).first().api_key
    session['department'] = 'student'
    return redirect('/')


@app.route('/loginpage', methods=['GET', 'POST'])
def login_page():
    return flask.render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/addlog', methods=['GET', 'POST'])
def add_log():
    school_id = flask.request.form.get('school_id')
    api_key = flask.request.form.get('api_key')

    # if not api_key or not School.query.filter_by(id=school_id, api_key=api_key):
    #     return SWJsonify({'Error': 'Unauthorized'}), 400

    id_no = flask.request.form.get('id_no')
    name = flask.request.form.get('name')
    level = flask.request.form.get('level')
    section = flask.request.form.get('section')
    date = flask.request.form.get('date')
    department = flask.request.form.get('department')
    time_in = flask.request.form.get('time_in')
    military_time = parse_date(flask.request.form.get('military_time'))

    add_this = Log(
            school_id=school_id,
            date=date,
            id_no=id_no,
            name=name,
            level=level,
            section=section,
            department=department,
            time_in=time_in,
            time_out='None',
            military_time=military_time,
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
    
    db.session.add(add_this)
    db.session.commit()

    return SWJsonify({
        'Status': 'Logged In',
        'Log': Log.query.all()
        }), 201


@app.route('/timeout', methods=['GET', 'POST'])
def time_out():
    school_id = flask.request.form.get('school_id')
    api_key = flask.request.form.get('api_key')

    if not api_key or not School.query.filter_by(id=school_id, api_key=api_key):
        return SWJsonify({'Error': 'Unauthorized'}), 400

    id_no = flask.request.form.get('id_no')
    time_out = flask.request.form.get('time_out')

    a = Log.query.filter_by(id_no=id_no).order_by(Log.timestamp.desc()).first()
    a.time_out=time_out  
    db.session.commit()

    return SWJsonify({
        'Status': 'Logged Out',
        'Log': Log.query.filter_by(id_no=id_no)\
        .order_by(Log.timestamp.desc()).first()
        }), 201


@app.route('/blast',methods=['GET','POST'])
def blast_message():
    for user in db.session.query(Student.parent_contact).distinct():
        print user.parent_contact   
    return flask.render_template('sending.html')


@app.route('/favicon.ico',methods=['GET','POST'])
def est():

    return('',204)



@app.route('/db/rebuild', methods=['GET', 'POST'])
def rebuild_database():
    db.drop_all()
    db.create_all()

    school = School(
        id=1234,
        api_key='ecc67d28db284a2fb351d58fe18965f9',
        password='test',
        name="Scuola Gesu Bambino",
        address="10, Brgy Isabang",
        city="Lucena City",
        email="sgb.edu@gmail.com",
        tel="555-8898",
        student_morning_start = now.replace(hour=8, minute=0, second=0),
        student_morning_end = now.replace(hour=12, minute=0, second=0),
        student_afternoon_start = now.replace(hour=13, minute=0, second=0),
        student_afternoon_end = now.replace(hour=16, minute=0, second=0),
        faculty_morning_start = now.replace(hour=7, minute=0, second=0),
        faculty_morning_end = now.replace(hour=12, minute=0, second=0),
        faculty_afternoon_start = now.replace(hour=13, minute=0, second=0),
        faculty_afternoon_end = now.replace(hour=16, minute=0, second=0)
        )

    a = Student(
        school_id=1234,
        id_no='2011334281',
        first_name='Jasper',
        last_name='Barcelona',
        middle_name='Estrada',
        level='2nd Grade',
        department='student',
        section='Fidelity',
        absences='0',
        lates='0',
        parent_contact='639183339068'
        )

    b = Student(
        school_id=1234,
        id_no='2011334282',
        first_name='Prof',
        last_name='Barcelona',
        middle_name='Estrada',
        department='faculty',
        absences='0',
        lates='0',
        parent_contact='639183339068'
        )

    db.session.add(school)
    db.session.add(a)
    db.session.add(b)
    db.session.commit()

    return SWJsonify({'Status': 'Database Rebuild Success'})


if __name__ == '__main__':
    app.debug = True
    app.run(port=int(os.environ['PORT']), host='0.0.0.0')

    # port=int(os.environ['PORT']), host='0.0.0.0'
