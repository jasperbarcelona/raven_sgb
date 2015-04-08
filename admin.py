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
import threading
from threading import Timer
import requests
import datetime
import time
import json
import uuid
import os


app = flask.Flask(__name__)
db = SQLAlchemy(app)
app.secret_key = '234234rfascasascqweqscasefsdvqwefe2323234dvsv'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
API_KEY = 'ecc67d28db284a2fb351d58fe18965f9'

SMS_URL = 'https://post.chikka.com/smsapi/request'
CLIENT_ID = 'ef8cf56d44f93b6ee6165a0caa3fe0d1ebeee9b20546998931907edbb266eb72'
SECRET_KEY = 'c4c461cc5aa5f9f89b701bc016a73e9981713be1bf7bb057c875dbfacff86e1d'
SHORT_CODE = '29290420420'
CONNECT_TIMEOUT = 5.0
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


class Student(db.Model, Serializer):
    __public__ = ['id','school_id','id_no','first_name','last_name','middle_name',
                  'level','department','section','absences','lates','parent_contact']

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer)
    id_no = db.Column(db.String(20))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    middle_name = db.Column(db.String(30))
    level = db.Column(db.String(30), default='None')
    department = db.Column(db.String(30))
    section = db.Column(db.String(30), default='None')
    absences = db.Column(db.String(3))
    lates = db.Column(db.String(3))
    parent_contact = db.Column(db.String(12))


class Late(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer)
    date = db.Column(db.String(20))
    id_no = db.Column(db.String(20))
    name = db.Column(db.String(60))
    level = db.Column(db.String(30))
    section = db.Column(db.String(30))
    time_in = db.Column(db.String(10))
    department = db.Column(db.String(30))
    timestamp = db.Column(db.String(50))


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
admin.add_view(IngAdmin(Late, db.session))


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


def get_student_data(id_no):
    return Student.query.filter_by(id_no=id_no).first()


def send_message(id_no, time, action):
    student = get_student_data(id_no)
    sendThis = 'Good day! We would like to inform you that '+student.first_name+' '+\
                student.last_name+' has ' + action +' the school gate at '+\
                time+'.'

    message_options = {
            'message_type': 'SEND',
            'message': sendThis,
            'client_id': CLIENT_ID,
            'mobile_number': get_student_data(id_no).parent_contact,
            'secret_key': SECRET_KEY,
            'shortcode': SHORT_CODE,
            'message_id': uuid.uuid4().hex
        }

    sent = False
    while not sent:
        try:
            r = requests.post(
                SMS_URL,
                message_options
                # timeout=(int(CONNECT_TIMEOUT))           
            )
            sent =True
            print r.text

        except requests.exceptions.ConnectionError as e:
            sleep(5)
            print "Too slow Mojo!"
            pass
    
    return None


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


def text_blast(message, contact):
    sendThis = message

    message_options = {
            'message_type': 'SEND',
            'message': sendThis,
            'client_id': CLIENT_ID,
            'mobile_number': contact,
            'secret_key': SECRET_KEY,
            'shortcode': SHORT_CODE,
            'message_id': uuid.uuid4().hex
        }

    sent = False
    while not sent:
        try:
            r = requests.post(
                SMS_URL,
                message_options
                # timeout=(int(CONNECT_TIMEOUT))           
            )
            sent =True
            print r.text

        except requests.exceptions.ConnectionError as e:
            sleep(5)
            print "Too slow Mojo!"
            pass
    
    return True


def check_if_late(school_id,api_key,id_no,name,level,section,date,department,time,military_time):
    time_now = str(now.replace(hour=get_hour(time), minute=int(time[3:5])))[11:]
    school = School.query.filter_by(api_key=api_key).first()

    if department == 'faculty':   
        morning_start = str(parse_date(school.faculty_morning_start))[11:]
        morning_end = str(parse_date(school.faculty_morning_end))[11:]
        afternoon_start = str(parse_date(school.faculty_afternoon_start))[11:]
        afternoon_end = str(parse_date(school.faculty_afternoon_end))[11:]

    else:
        morning_start = str(parse_date(school.student_morning_start))[11:]
        morning_end = str(parse_date(school.student_morning_end))[11:]
        afternoon_start = str(parse_date(school.student_afternoon_start))[11:]
        afternoon_end = str(parse_date(school.student_afternoon_end))[11:]
    
    if (time_now >= morning_start and time_now < morning_end) or \
       (time_now >= afternoon_start and time_now < afternoon_end):

       late = Late(
            school_id=school_id,
            date=date,
            id_no=id_no,
            name=name,
            level=level,
            section=section,
            time_in=time,
            department=department,
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )

       db.session.add(late)
       db.session.commit()
       lates=Student.query.filter_by(id_no=id_no).first().lates
       lates=Late.query.filter_by(id_no=id_no).count()
       db.session.commit()


def time_in(school_id,api_key,id_no,name,level,section,date,department,time,military_time):
    add_this = Log(
                    school_id=school_id,
                    date=date,
                    id_no=id_no,
                    name=name,
                    level=level,
                    section=section,
                    department=department,
                    time_in=time,
                    time_out='None',
                    military_time=military_time,
                    timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                    )

    db.session.add(add_this)
    db.session.commit()

    message_thread = threading.Thread(target=send_message,args=[id_no, time, 'entered'])    
    message_thread.start()

    check_if_late(school_id,api_key,id_no,name,level,section,date,department,time,military_time)
            
    return SWJsonify({
        'Status': 'Logged In',
        'Log': Log.query.all()
        }), 201


def time_ou(id_no, time):
    a = Log.query.filter_by(id_no=id_no).order_by(Log.timestamp.desc()).first()
    a.time_out=time  
    db.session.commit()

    message_thread = threading.Thread(target=send_message,args=[id_no, time, 'exited'])    
    message_thread.start()

    return SWJsonify({
        'Status': 'Logged Out',
        'Log': Log.query.filter_by(id_no=id_no)\
        .order_by(Log.timestamp.desc()).first()
        }), 201


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

    l = Late.query.filter_by(
        school_id=session['school_id'],
        department=session['department']
        ).order_by(Late.timestamp.desc()).all()

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

    if not api_key or not School.query.filter_by(id=school_id, api_key=api_key):
        return SWJsonify({'Error': 'Unauthorized'}), 400

    id_no = flask.request.form.get('id_no')
    name = flask.request.form.get('name')
    level = flask.request.form.get('level')
    section = flask.request.form.get('section')
    date = flask.request.form.get('date')
    department = flask.request.form.get('department')
    time = flask.request.form.get('time')
    military_time = parse_date(flask.request.form.get('military_time'))

    if not Log.query.filter_by(date=date, id_no=id_no).first() or Log.query.filter_by\
    (date=date, id_no=id_no).order_by(Log.timestamp.desc()).first().time_out != 'None':
        time_in_thread = threading.Thread(target=time_in,args=[school_id,api_key,id_no,name,level,section,date,department,time,military_time])    
     
        return time_in_thread.start()
    return time_out(id_no, time)


@app.route('/blast',methods=['GET','POST'])
def blast_message():
    message = flask.request.form.get('message')
    for user in db.session.query(Student.parent_contact).distinct():
        text_blast(message, user.parent_contact) 
    return flask.render_template('status.html')


@app.route('/sync',methods=['GET','POST'])
def sync_database():
    school_id = flask.request.args.get('school_id')
    return SWJsonify({
        'Records': Student.query.filter_by(school_id=school_id).all()
        }), 201


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
        student_afternoon_end = now.replace(hour=17, minute=0, second=0),
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
