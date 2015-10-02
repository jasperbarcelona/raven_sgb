import flask, flask.views
from flask import url_for, request, session, redirect, jsonify, Response, make_response, current_app
from jinja2 import environment, FileSystemLoader
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import Boolean
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
from multiprocessing.pool import ThreadPool
from time import sleep
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

PRIMARY = ['1st Grade', '2nd Grade', '3rd Grade', '4th Grade', '5th Grade', '6th Grade']
JUNIOR_HIGH = ['7th Grade', '8th Grade', '9th Grade', '10th Grade']
SENIOR_HIGH = ['11th Grade', '12th Grade']
# os.environ['DATABASE_URL']
# 'sqlite:///local.db'

now = datetime.datetime.now()
pool = ThreadPool(processes=1)


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

    primary_morning_class = db.Column(Boolean, unique=False)
    primary_afternoon_class = db.Column(Boolean, unique=False)
    junior_morning_class = db.Column(Boolean, unique=False)
    junior_afternoon_class = db.Column(Boolean, unique=False)
    senior_morning_class = db.Column(Boolean, unique=False)
    senior_afternoon_class = db.Column(Boolean, unique=False)

    primary_morning_start = db.Column(db.String(30))
    primary_morning_end = db.Column(db.String(30))
    primary_afternoon_start = db.Column(db.String(30))
    primary_afternoon_end = db.Column(db.String(30))
    junior_morning_start = db.Column(db.String(30))
    junior_morning_end = db.Column(db.String(30))
    junior_afternoon_start = db.Column(db.String(30))
    junior_afternoon_end = db.Column(db.String(30))
    senior_morning_start = db.Column(db.String(30))
    senior_morning_end = db.Column(db.String(30))
    senior_afternoon_start = db.Column(db.String(30))
    senior_afternoon_end = db.Column(db.String(30))


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer)
    name = db.Column(db.String(30))


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
    date = db.Column(db.String(20))
    id_no = db.Column(db.String(20))
    name = db.Column(db.String(60))
    level = db.Column(db.String(30))
    section = db.Column(db.String(30))
    department = db.Column(db.String(30))
    time_of_day = db.Column(db.String(20))
    timestamp = db.Column(db.String(50))


class IngAdmin(sqla.ModelView):
    column_display_pk = True
admin = Admin(app, name='raven')
admin.add_view(IngAdmin(School, db.session))
admin.add_view(IngAdmin(Section, db.session))
admin.add_view(IngAdmin(Log, db.session))
admin.add_view(IngAdmin(Student, db.session))
admin.add_view(IngAdmin(Late, db.session))
admin.add_view(IngAdmin(Absent, db.session))


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
        return hour
    elif time[6:8] == 'AM' and time[:2] == '12':
        hour = 00
        return hour
    hour = int(time[:2])
    return hour


def get_student_data(id_no):
    return Student.query.filter_by(id_no=id_no).first()


def message_options(message, msisdn):
    message_options = {
            'message_type': 'SEND',
            'message': message,
            'client_id': CLIENT_ID,
            'mobile_number': msisdn,
            'secret_key': SECRET_KEY,
            'shortcode': SHORT_CODE,
            'message_id': uuid.uuid4().hex
        }
    return message_options


def send_message(type, message, msisdn, request_url):
    sent = False
    while not sent:
        try:
            r = requests.post(
                request_url,
                message_options(message, msisdn)
                # timeout=(int(CONNECT_TIMEOUT))           
            )
            sent = True
            print r.status_code #update log database (put 'sent' to status)

        except requests.exceptions.ConnectionError as e:
            print "Sending Failed!"
            sleep(5)


def authenticate_user(school_id, password):
    if not School.query.filter_by(id=school_id, password=password).first():
        return False
    return True


def mark_morning_absent(school_id,api_key):
    all_students = Student.query.filter_by(school_id=school_id).all()

    for student in all_students:
        logged = Log.query.filter_by(date=time.strftime("%B %d, %Y"),id_no=student.id_no).order_by(Log.timestamp.desc()).first()
        if logged == None or logged.time_out != 'None':
            absent = Absent(
            school_id=school_id,
            date=time.strftime("%B %d, %Y"),
            id_no=student.id_no,
            name=student.last_name+', '+\
                         student.first_name+' '+\
                         student.middle_name[:1]+'.',
            level=student.level,
            section=student.section,
            department=student.department,
            time_of_day='morning',
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )

            db.session.add(absent)
            db.session.commit()

            student.absences=Absent.query.filter_by(id_no=student.id_no, school_id=school_id).count()
            db.session.commit()


def mark_afternoon_absent(school_id,api_key):
    all_students = Student.query.filter_by(school_id=school_id).all()

    for student in all_students:
        logged = Log.query.filter_by(date=time.strftime("%B %d, %Y"),id_no=student.id_no).order_by(Log.timestamp.desc()).first()
        if not logged or logged.time_out != 'None':
            absent = Absent(
            school_id=school_id,
            date=time.strftime("%B %d, %Y"),
            id_no=student.id_no,
            name=student.last_name+', '+\
                         student.first_name+' '+\
                         student.middle_name[:1]+'.',
            level=student.level,
            section=student.section,
            department=student.department,
            time_of_day='afternoon',
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )

            db.session.add(absent)
            db.session.commit()

            student.absences=Absent.query.filter_by(id_no=student.id_no, school_id=school_id).count()
            db.session.commit()

def mark_specific_absent(school_id,id_no,time_of_day):
    student = Student.query.filter_by(school_id=school_id,id_no=id_no).first()
    absent = Absent(
            school_id=school_id,
            date=time.strftime("%B %d, %Y"),
            id_no=id_no,
            name=student.last_name+', '+\
                         student.first_name+' '+\
                         student.middle_name[:1]+'.',
            level=student.level,
            section=student.section,
            department=student.department,
            time_of_day=time_of_day,
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
    db.session.add(absent)
    db.session.commit()

    student.absences=Absent.query.filter_by(id_no=id_no, school_id=school_id).count()
    db.session.commit()


def check_if_late(school_id,api_key,id_no,name,level,
                section,date,department,time,timestamp):

    time_now = str(now.replace(hour=get_hour(time), minute=int(time[3:5])))[11:16]
    school = School.query.filter_by(api_key=api_key).first()

    if level in PRIMARY:
        educ = 'primary'
    elif level in JUNIOR_HIGH:
        educ = 'junior'
    elif level in SENIOR_HIGH:
        educ = 'senior'

    query = 'school.%s' %educ

    morning_start = eval(query+'_morning_start')
    morning_end = eval(query+'_morning_end')
    afternoon_start = eval(query+'_afternoon_start')
    afternoon_end = eval(query+'_afternoon_end')

    # if ((parse_date(time_now) >= parse_date(morning_start) and parse_date(time_now) < parse_date(morning_end)) or \
    #     (parse_date(time_now) >= parse_date(afternoon_start) and parse_date(time_now) < parse_date(afternoon_end))) and\
    #     Absent.query.filter_by(school_id=school_id,id_no=id_no,date=date).first() == None:

    #     record_as_late(school_id, id_no, name, level, section, 
    #                    date, department, time)

    if parse_date(time_now) >= parse_date(morning_start) and\
        parse_date(time_now) < parse_date(morning_end) and\
        Absent.query.filter_by(school_id=school_id,id_no=id_no,date=date,time_of_day='morning').first() == None:

        if str(parse_date(time_now) - parse_date(morning_start)) > '1:00:00':
            mark_specific_absent(school_id,id_no,'morning')
        else:
            record_as_late(school_id, id_no, name, level, section, 
                        date, department, time, timestamp)

    elif (parse_date(time_now) >= parse_date(afternoon_start) and\
        parse_date(time_now) < parse_date(afternoon_end)) and\
        Absent.query.filter_by(school_id=school_id,id_no=id_no,date=date,time_of_day='afternoon').first() == None:

        if str(parse_date(time_now) - parse_date(afternoon_start)) > '1:00:00':
            mark_specific_absent(school_id,id_no,'afternoon')
        else:
            record_as_late(school_id, id_no, name, level, section, 
                        date, department, time, timestamp)


def record_as_late(school_id, id_no, name, level, section, 
                    date, department, time, timestamp):
    late = Late(
            school_id=school_id,date=date,id_no=id_no,
            name=name,level=level,section=section,
            time_in=time,department=department,
            timestamp=timestamp
            )

    db.session.add(late)
    db.session.commit()

    student=Student.query.filter_by(id_no=id_no, school_id=school_id).one()
    student.lates=Late.query.filter_by(id_no=id_no, school_id=school_id).count()
    db.session.commit()


def time_in(school_id,api_key,id_no,name,level,section,
            date,department,time,timestamp):

    add_this = Log(
        school_id=school_id,date=date,id_no=id_no,
        name=name,level=level,section=section,
        department=department,time_in=time,
        time_out='None',timestamp=timestamp
        )

    db.session.add(add_this)
    db.session.commit()

    compose_message(id_no,time,'entered')

    if department != 'faculty':
        return check_if_late(school_id, api_key, id_no,name,level,
                  section, date, department, time, timestamp)

    return '', 201


def compose_message(id_no,time,action):
    # student = get_student_data(id_no)
    # message = 'Good day! We would like to inform you that '+student.first_name+' '+\
    #             student.last_name+' has '+action+' the school gate at '+\
    #             time+'.'

    # message_thread = threading.Thread(
    #     target=send_message,
    #     args=[
    #         'log',
    #         message,
    #         student.parent_contact,
    #         SMS_URL
    #         ]
    #     )
    # message_thread.start()
    print 'done'


def time_out(id_no, time, school_id):
    a = Log.query.filter_by(id_no=id_no,school_id=school_id).order_by(Log.timestamp.desc()).first()
    a.time_out=time  
    db.session.commit()

    compose_message(id_no,time,'exited')

    return '', 201


def prepare():
    global variable
    session['logs_limit']+=100
    session['late_limit']+=100
    session['attendance_limit']+=100
    variable = pool.apply_async(fetch_next, (session['logs_limit'],
                      session['late_limit'],session['attendance_limit'],
                      session['absent_limit'],session['school_id'],
                      session['department'])).get()


def fetch_first(logs_limit, late_limit, attendance_limit, absent_limit, school_id, department):
     logs = Log.query.filter_by(
        school_id=school_id,
        department=department
        ).order_by(Log.timestamp.desc()).slice((logs_limit-100),logs_limit)

     late = Late.query.filter_by(
        school_id=school_id,
        department=department
        ).order_by(Late.timestamp.desc()).slice((late_limit-100),late_limit)

     attendance = Student.query.filter_by(
        school_id=school_id,
        department=department)\
        .order_by(Student.last_name).slice((attendance_limit-100),attendance_limit)

     absent = Absent.query.filter_by(
        school_id=school_id,
        department=department)\
        .order_by(Absent.date.desc()).slice((absent_limit-100),absent_limit)

     return {'logs':logs, 'late':late, 'attendance':attendance, 'absent':absent}


def fetch_next(needed,limit):
    if needed == 'logs':
        search_table = 'Log'
        sort_by = 'timestamp'
        sort_type='.desc()'

    elif needed == 'late':
        search_table = 'Late'
        sort_by = 'timestamp'
        sort_type='.desc()'

    elif needed == 'attendance':
        search_table = 'Student'
        sort_by = 'last_name'
        sort_type=''

    elif needed == 'absent':
        search_table = 'Absent'
        sort_by = 'timestamp'
        sort_type='.desc()'

    session[needed+'_limit'] += 100
    result = eval(search_table+'.query.filter_by(school_id=session[\'school_id\'],department=session[\'department\']).order_by('+search_table+'.'+sort_by+sort_type+').slice((session[\''+needed+'_limit\']-100),session[\''+needed+'_limit\'])')

    return result


def search_logs(*args, **kwargs):
    query = 'Log.query.filter('
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Log.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Log.timestamp.desc()).slice(('+str(args[0])+'-100),'+str(args[0])+')'
    session['logs_search_limit']+=100
    return eval(query)


def search_attendance(*args, **kwargs):
    query = 'Student.query.filter('
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Student.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Student.last_name).slice(('+str(args[0])+'-100),'+str(args[0])+')'
    session['attendance_search_limit']+=100
    return eval(query)


def search_absent(*args, **kwargs):
    query = 'Absent.query.filter('
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Absent.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Absent.name).slice(('+str(args[0])+'-100),'+str(args[0])+')'
    session['absent_search_limit']+=100
    return eval(query)


def search_late(*args, **kwargs):
    query = 'Late.query.filter('
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Late.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Late.name).slice(('+str(args[0])+'-100),'+str(args[0])+')'
    session['late_search_limit']+=100

    print 'xxxxxxxxxxxxxxxxxxx'
    print query

    return eval(query)


def get_latest_schedule(api_key):
    school = School.query.filter_by(api_key=api_key).first()

    if school == None:
        return {
            'status': 'Failed',
            'message': 'School not found',
            }

    primary_morning_start = school.primary_morning_start
    junior_morning_start = school.junior_morning_start
    senior_morning_start = school.senior_morning_start

    primary_afternoon_start = school.primary_afternoon_start
    junior_afternoon_start = school.junior_afternoon_start
    senior_afternoon_start = school.senior_afternoon_start


    if (primary_morning_start > junior_morning_start) and (primary_morning_start > senior_morning_start):
        morning_time = primary_morning_start
    elif (junior_morning_start > primary_morning_start) and (junior_morning_start > senior_morning_start):
        morning_time = junior_morning_start
    else:
        morning_time = senior_morning_start

    if (primary_afternoon_start > junior_afternoon_start) and (primary_afternoon_start > senior_afternoon_start):
        afternoon_time = primary_afternoon_start
    elif (junior_afternoon_start > primary_afternoon_start) and (junior_afternoon_start > senior_afternoon_start):
        afternoon_time = junior_afternoon_start
    else:
        afternoon_time = senior_afternoon_start

    return jsonify(
        status= 'success',
        morning_time= morning_time,
        afternoon_time= afternoon_time
        )


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")


@app.route('/sched/get', methods=['GET', 'POST'])
def get_schedule():
    api_key = flask.request.args.get('api_key')
    return get_latest_schedule(api_key)


@app.route('/', methods=['GET', 'POST'])
def index():
    if not session:
        return redirect('/loginpage')
    session['logs_limit'] = 100
    session['late_limit'] = 100
    session['attendance_limit'] = 100
    session['absent_limit'] = 100
    session['logs_search_limit'] = 100
    session['attendance_search_limit'] = 100
    session['late_search_limit'] = 100
    session['absent_search_limit'] = 100

    school = School.query.filter_by(api_key=session['api_key']).one()
    sections = Section.query.filter_by(school_id=session['school_id']).all()

    first_set = fetch_first(session['logs_limit'],session['late_limit'],
        session['attendance_limit'],session['absent_limit'],session['school_id'],
        session['department'])

    # prepare()

    return flask.render_template(
        'index.html',
        log=first_set['logs'],
        late=first_set['late'],
        attendance=first_set['attendance'],
        absent=first_set['absent'], 
        view=session['department'],
        sections=sections,
        primary_morning_start=school.primary_morning_start,
        primary_morning_end=school.primary_morning_end,
        primary_afternoon_start=school.primary_afternoon_start,
        primary_afternoon_end=school.primary_afternoon_end,
        junior_morning_start=school.junior_morning_start,
        junior_morning_end=school.junior_morning_end,
        junior_afternoon_start=school.junior_afternoon_start,
        junior_afternoon_end=school.junior_afternoon_end,
        senior_morning_start=school.senior_morning_start,
        senior_morning_end=school.senior_morning_end,
        senior_afternoon_start=school.senior_afternoon_start,
        senior_afternoon_end=school.senior_afternoon_end,
        tab=session['tab'],
        path='../images/watermark.png'
        )


@app.route('/rollback', methods=['GET', 'POST'])
def rollback():
    db.session.rollback()
    return 'ok'


@app.route('/home', methods=['GET', 'POST'])
def start_again():
    needed = flask.request.form.get('tab') 

    session[needed+'_limit'] = 0
    
    session[needed+'_search_limit'] = 100

    data = fetch_next(needed,0)

    # prepare()

    return flask.render_template(needed+'.html', data=data, limit=0, view=session['department'])


@app.route('/loadmore', methods=['GET', 'POST'])
def load_more():
    needed = flask.request.form.get('data')

    if needed == 'logs':
        data = fetch_next(needed,session['logs_limit'])
        page = 'logs.html'
        limit = session['logs_limit']-100
    elif needed == 'late':
        data = fetch_next(needed,session['late_limit'])
        page = 'late.html'
        limit = session['late_limit']-100
        
    elif needed == 'absent':
        data = fetch_next(needed,session['absent_limit'])
        page = 'absent.html'
        limit = session['absent_limit']-100

    elif needed == 'attendance':
        data = fetch_next(needed,session['attendance_limit'])
        page = 'attendance.html'
        limit = session['attendance_limit']-100
        
    # prepare()

    return flask.render_template(
        page,
        data=data,
        limit=limit,
        view=session['department']
        )


@app.route('/view', methods=['GET', 'POST'])
def change_view():
    view = flask.request.args.get('view')
    session['department'] = view
    return redirect('/')


@app.route('/absent/morning/mark', methods=['GET', 'POST'])
def mark_absent_morning():
    school_id = flask.request.form.get('school_id')
    api_key = flask.request.form.get('api_key')

    if not api_key or not School.query.filter_by(id=school_id, api_key=api_key):
        return primary_morning_start

    mark_morning_absent(school_id,api_key)
    return '',201


@app.route('/absent/afternoon/mark', methods=['GET', 'POST'])
def mark_absent_afternoon():
    school_id = flask.request.form.get('school_id')
    api_key = flask.request.form.get('api_key')

    if not api_key or not School.query.filter_by(id=school_id, api_key=api_key):
        return primary_morning_start

    mark_afternoon_absent(school_id,api_key)
    return '',201


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
    session['tab'] = 'logs'
    return redirect('/')


@app.route('/loginpage', methods=['GET', 'POST'])
def login_page():
    if session:
        return redirect('/')
    return flask.render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/student/info/get', methods=['GET', 'POST'])
def get_student_info():
    student_id = flask.request.form.get('student_id')
    student = Student.query.filter_by(id=student_id).first()
    sections = Section.query.filter_by(school_id=session['school_id']).all()
    return flask.render_template('student_info.html', student=student, sections=sections)


@app.route('/tab/change', methods=['GET', 'POST'])
def change_tab():
    tab = flask.request.form.get('tab')
    session['tab'] = tab
    return '',200


@app.route('/addlog', methods=['POST'])
def add_log():
    sleep(1)
    data = flask.request.form.to_dict()

    if not data['api_key'] or not School.query.filter_by(id=data['school_id'],api_key=data['api_key']):
        return jsonify(status='500',message='Unauthorized'), 500

    logged = Log.query.filter_by(date=data['date'],school_id=data['school_id'],id_no=data['id_no']).order_by(Log.timestamp.desc()).first()

    if not logged or logged.time_out != 'None':

        log_thread = threading.Thread(
            target=time_in,
            args=[
            data['school_id'],data['api_key'],
            data['id_no'],data['name'],data['level'],
            data['section'],data['date'],data['department'],
            data['time'],data['timestamp']
            ])

        log_thread.start()     

        return jsonify(status= '201',message= 'Looged In'), 201

    log_thread = threading.Thread(target=time_out,args=[data['id_no'],data['time'],data['school_id']])
    log_thread.start()      

    return jsonify(status='201',message='Looged Out'), 201


@app.route('/blast',methods=['GET','POST'])
def blast_message():
    password = flask.request.form.get('password')
    message = flask.request.form.get('message')
    if not authenticate_user(session['school_id'], password):
        return flask.render_template('status.html', status='Unauthorized')

    for user in db.session.query(Student.parent_contact).filter\
              (Student.school_id==session['school_id']).distinct(): 

        blast_thread = threading.Thread(
            target=send_message,
            args=[
                'blast',
                message,
                user.parent_contact,
                SMS_URL
                ]
            )
        blast_thread.start()
    
    return flask.render_template('status.html', status='Message Sent')


@app.route('/sync',methods=['GET','POST'])
def sync_database():
    school_id = flask.request.args.get('school_id')
    return SWJsonify({
        'Records': Student.query.filter_by(school_id=school_id).all()
        }), 201


@app.route('/user/add',methods=['GET','POST'])
def add_user():
    last_name = flask.request.form.get('last_name')
    first_name = flask.request.form.get('first_name')
    middle_name = flask.request.form.get('middle_name')
    level = flask.request.form.get('level')
    section = flask.request.form.get('section')
    contact = flask.request.form.get('contact')
    id_no = flask.request.form.get('id_no')

    user = Student(
        school_id = session['school_id'],
        id_no = id_no,
        first_name = first_name,
        last_name = last_name,
        middle_name = middle_name,
        level = level,
        department = session['department'],
        section = section,
        absences = 0,
        lates = 0,
        parent_contact = contact
        )

    db.session.add(user)
    db.session.commit()

    session['attendance_limit'] = 0
    
    session['attendance_search_limit'] = 100

    data = fetch_next('attendance',0)

    # prepare()

    return flask.render_template('attendance.html', data=data, limit=0)


@app.route('/user/edit',methods=['GET','POST'])
def edit_user():

    last_name = flask.request.form.get('last_name')
    first_name = flask.request.form.get('first_name')
    middle_name = flask.request.form.get('middle_name')
    level = flask.request.form.get('level')
    section = flask.request.form.get('section')
    contact = flask.request.form.get('contact')
    id_no = flask.request.form.get('id_no')
    user_id = flask.request.form.get('user_id')

    user = Student.query.filter_by(id=user_id).first()
    user.last_name = last_name
    user.first_name = first_name
    user.middle_name = middle_name
    user.level = level
    user.section = section
    user.parent_contact = contact
    user.id_no = id_no

    db.session.commit()

    session['attendance_limit'] = 0
    
    session['attendance_search_limit'] = 100

    data = fetch_next('attendance',0)

    # prepare()

    return flask.render_template('attendance.html', data=data, limit=0)


@app.route('/search/logs',methods=['GET','POST'])
def search_student_logs():
    needed = flask.request.form.get('needed')
    date = flask.request.form.get('date')
    id_no = flask.request.form.get('id_no')
    name = flask.request.form.get('name')
    level = flask.request.form.get('level')
    section = flask.request.form.get('section')
    reset = flask.request.form.get('reset')

    if reset == 'yes':
        session['logs_search_limit']=100
    
    limit = session['logs_search_limit']-100
    
    data = search_logs(session['logs_search_limit'],date=date, id_no=id_no,
                       name=name, level=level,
                       section=section)

    return flask.render_template(
        needed+'.html',
        data=data,
        view=session['department'],
        limit=limit
        )


@app.route('/search/attendance',methods=['GET','POST'])
def search_student_attendance():
    needed = flask.request.form.get('needed')
    last_name = flask.request.form.get('last_name')
    first_name = flask.request.form.get('first_name')
    middle_name = flask.request.form.get('middle_name')
    id_no = flask.request.form.get('id_no')
    level = flask.request.form.get('level')
    section = flask.request.form.get('section')
    absences = flask.request.form.get('absences')
    lates = flask.request.form.get('lates')
    reset = flask.request.form.get('reset')

    if reset == 'yes':
        session['attendance_search_limit']=100
    
    limit = session['attendance_search_limit']-100
    
    data = search_attendance(session['attendance_search_limit'],last_name=last_name, first_name=first_name,
                middle_name=middle_name, id_no=id_no, level=level, section=section,
                absences=absences, lates=lates)

    return flask.render_template(
        needed+'.html',
        data=data,
        view=session['department'],
        limit=limit
        )


@app.route('/search/absent',methods=['GET','POST'])
def search_student_absent():
    needed = flask.request.form.get('needed')
    date = flask.request.form.get('date')
    id_no = flask.request.form.get('id_no')
    name = flask.request.form.get('name')
    level = flask.request.form.get('level')
    section = flask.request.form.get('section')
    reset = flask.request.form.get('reset')

    if reset == 'yes':
        session['absent_search_limit']=100
    
    limit = session['absent_search_limit']-100
    
    data = search_absent(session['absent_search_limit'], date=date, id_no=id_no,
                       name=name, level=level,
                       section=section)

    return flask.render_template(
        needed+'.html',
        data=data,
        view=session['department'],
        limit=limit
        )


@app.route('/search/late',methods=['GET','POST'])
def search_student_late():
    needed = flask.request.form.get('needed')
    date = flask.request.form.get('date')
    id_no = flask.request.form.get('id_no')
    name = flask.request.form.get('name')
    level = flask.request.form.get('level')
    section = flask.request.form.get('section')
    reset = flask.request.form.get('reset')

    if reset == 'yes':
        session['late_search_limit']=100
    
    limit = session['late_search_limit']-100
    
    data = search_late(session['late_search_limit'], date=date, id_no=id_no,
                       name=name, level=level,
                       section=section)

    return flask.render_template(
        needed+'.html',
        data=data,
        view=session['department'],
        limit=limit
        )


@app.route('/sched',methods=['GET','POST'])
def change_sched():

    primary_morning_start = flask.request.form.get('primary_morning_start')
    primary_morning_end = flask.request.form.get('primary_morning_end')
    junior_morning_start = flask.request.form.get('junior_morning_start')
    junior_morning_end = flask.request.form.get('junior_morning_end')
    senior_morning_start = flask.request.form.get('senior_morning_start')
    senior_morning_end = flask.request.form.get('senior_morning_end')
    primary_afternoon_start = flask.request.form.get('primary_afternoon_start')
    primary_afternoon_end = flask.request.form.get('primary_afternoon_end')
    junior_afternoon_start = flask.request.form.get('junior_afternoon_start')
    junior_afternoon_end = flask.request.form.get('junior_afternoon_end')
    senior_afternoon_start = flask.request.form.get('senior_afternoon_start')
    senior_afternoon_end = flask.request.form.get('senior_afternoon_end')

    school = School.query.filter_by(id=session['school_id']).one()

    school.primary_morning_start = primary_morning_start
    school.primary_morning_end = primary_morning_end
    school.junior_morning_start = junior_morning_start
    school.junior_morning_end = junior_morning_end
    school.senior_morning_start = senior_morning_start
    school.senior_morning_end = senior_morning_end
    school.primary_afternoon_start = primary_afternoon_start
    school.primary_afternoon_end = primary_afternoon_end
    school.junior_afternoon_start = junior_afternoon_start
    school.junior_afternoon_end = junior_afternoon_end
    school.senior_afternoon_start = senior_afternoon_start
    school.senior_afternoon_end = senior_afternoon_end

    db.session.commit()

    sched_data = {
        'school_id': session['school_id'],
        'primary_morning_start': primary_morning_start,
        'primary_morning_end': primary_morning_end,
        'junior_morning_start': junior_morning_start,
        'junior_morning_end': junior_morning_end,
        'senior_morning_start': senior_morning_start,
        'senior_morning_end': senior_morning_end,
        'primary_afternoon_start': primary_afternoon_start,
        'primary_afternoon_end':primary_afternoon_end,
        'junior_afternoon_start': junior_afternoon_start,
        'junior_afternoon_end': junior_afternoon_end,
        'senior_afternoon_start': senior_afternoon_start,
        'senior_afternoon_end': senior_afternoon_end
    }

    sent = False
    while not sent:
        try:
            r = requests.post(
                'http://127.0.0.1:8000/schedule/regular/update',
                sched_data         
            )
            sent =True
            print r.status_code #update log database (put 'sent' to status)

        except requests.exceptions.ConnectionError as e:
            sleep(5)
            print "Disconnected!"
            pass

    return redirect('/')


@app.route('/id/validate',methods=['GET','POST'])
def validate_id():
    id_no = flask.request.form.get('id_no')
    student = Student.query.filter_by(id_no=id_no).first()
    if student != None:
        error = 1
    else:
        error = 0
    return flask.render_template('validate_id.html',error=error,id_no=id_no)


@app.route('/favicon.ico',methods=['GET','POST'])
def est():
    return '',204


@app.route('/schedule/sync',methods=['GET','POST'])
def sync_schedule():
    data = flask.request.form.to_dict()

    school = School.query.filter_by(id=data['school_id']).one()

    school.primary_morning_class = str2bool(data['primary_morning_class'])
    school.primary_afternoon_class = str2bool(data['primary_afternoon_class'])
    school.junior_morning_class = str2bool(data['junior_morning_class'])
    school.junior_afternoon_class = str2bool(data['junior_afternoon_class'])
    school.senior_morning_class = str2bool(data['senior_morning_class'])
    school.senior_afternoon_class = str2bool(data['senior_afternoon_class'])

    school.primary_morning_start = data['primary_morning_start']
    school.primary_morning_end = data['primary_morning_end']
    school.junior_morning_start = data['junior_morning_start']
    school.junior_morning_end = data['junior_morning_end']
    school.senior_morning_start = data['senior_morning_start']
    school.senior_morning_end = data['senior_morning_end']
    school.primary_afternoon_start = data['primary_afternoon_start']
    school.primary_afternoon_end = data['primary_afternoon_end']
    school.junior_afternoon_start = data['junior_afternoon_start']
    school.junior_afternoon_end = data['junior_afternoon_end']
    school.senior_afternoon_start = data['senior_afternoon_start']
    school.senior_afternoon_end = data['senior_afternoon_end']

    db.session.commit()
    return '',201


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

        primary_morning_start = str(now.replace(hour=7, minute=0, second=0))[11:16],
        primary_morning_end = str(now.replace(hour=12, minute=0, second=0))[11:16],
        primary_afternoon_start = str(now.replace(hour=13, minute=0, second=0))[11:16],
        primary_afternoon_end = str(now.replace(hour=18, minute=0, second=0))[11:16],

        junior_morning_start = str(now.replace(hour=8, minute=0, second=0))[11:16],
        junior_morning_end = str(now.replace(hour=12, minute=0, second=0))[11:16],
        junior_afternoon_start = str(now.replace(hour=13, minute=0, second=0))[11:16],
        junior_afternoon_end = str(now.replace(hour=16, minute=0, second=0))[11:16],

        senior_morning_start = str(now.replace(hour=9, minute=0, second=0))[11:16],
        senior_morning_end = str(now.replace(hour=12, minute=0, second=0))[11:16],
        senior_afternoon_start = str(now.replace(hour=13, minute=0, second=0))[11:16],
        senior_afternoon_end = str(now.replace(hour=16, minute=0, second=0))[11:16]
        )
    db.session.add(school)

    school1 = School(
        id=4321,
        api_key='ecc67d28db284a2fb351d58fe18965f0',
        password='test',
        name="Sacred Heart College",
        address="10, Brgy Isabang",
        city="Lucena City",
        email="sgb.edu@gmail.com",
        tel="555-8898",

        primary_morning_start = str(now.replace(hour=7, minute=0, second=0))[11:16],
        primary_morning_end = str(now.replace(hour=12, minute=0, second=0))[11:16],
        primary_afternoon_start = str(now.replace(hour=13, minute=0, second=0))[11:16],
        primary_afternoon_end = str(now.replace(hour=18, minute=0, second=0))[11:16],

        junior_morning_start = str(now.replace(hour=8, minute=0, second=0))[11:16],
        junior_morning_end = str(now.replace(hour=12, minute=0, second=0))[11:16],
        junior_afternoon_start = str(now.replace(hour=13, minute=0, second=0))[11:16],
        junior_afternoon_end = str(now.replace(hour=16, minute=0, second=0))[11:16],

        senior_morning_start = str(now.replace(hour=9, minute=0, second=0))[11:16],
        senior_morning_end = str(now.replace(hour=12, minute=0, second=0))[11:16],
        senior_afternoon_start = str(now.replace(hour=13, minute=0, second=0))[11:16],
        senior_afternoon_end = str(now.replace(hour=16, minute=0, second=0))[11:16]
        )
    db.session.add(school1)

    a = Student(
        school_id=1234,
        id_no='2011334281',
        first_name='Jasper',
        last_name='Barcelona',
        middle_name='Estrada',
        level='2nd Grade',
        department='student',
        section='Charity',
        absences='0',
        lates='0',
        parent_contact='639183339068'
        )
    b = Student(
        school_id=1234,
        id_no='2011334282',
        first_name='Janno',
        last_name='Armamento',
        middle_name='Estrada',
        level='8th Grade',
        department='student',
        section='Fidelity',
        absences='0',
        lates='0',
        parent_contact='639183339068'
        )

    c = Student(
        school_id=1234,
        id_no='2011334283',
        first_name='Bear',
        last_name='Delos Reyes',
        middle_name='Estrada',
        level='12th Grade',
        department='student',
        section='Fidelity',
        absences='0',
        lates='0',
        parent_contact='639183339068'
        )

    d = Section(
        school_id=1234,
        name='Charity'
        )

    e = Section(
        school_id=1234,
        name='Fidelity'
        )

    f = Section(
        school_id=1234,
        name='Peace'
        )

    db.session.add(a)
    db.session.add(b)
    db.session.add(c)
    db.session.add(d)
    db.session.add(e)
    db.session.add(f)
    db.session.commit()
    return SWJsonify({'status': 'Database Rebuild Success'})

# @app.route('/db/rebuild', methods=['GET', 'POST'])
# def rebuild_database():
#     db.drop_all()
#     db.create_all()

#     school = School(
#         id=1234,
#         api_key='ecc67d28db284a2fb351d58fe18965f9',
#         password='test',
#         name="Scuola Gesu Bambino",
#         address="10, Brgy Isabang",
#         city="Lucena City",
#         email="sgb.edu@gmail.com",
#         tel="555-8898",

#         primary_morning_start = str(now.replace(hour=7, minute=0, second=0))[11:16],
#         primary_morning_end = str(now.replace(hour=12, minute=0, second=0))[11:16],
#         primary_afternoon_start = str(now.replace(hour=13, minute=0, second=0))[11:16],
#         primary_afternoon_end = str(now.replace(hour=18, minute=0, second=0))[11:16],

#         junior_morning_start = str(now.replace(hour=8, minute=0, second=0))[11:16],
#         junior_morning_end = str(now.replace(hour=12, minute=0, second=0))[11:16],
#         junior_afternoon_start = str(now.replace(hour=13, minute=0, second=0))[11:16],
#         junior_afternoon_end = str(now.replace(hour=16, minute=0, second=0))[11:16],

#         senior_morning_start = str(now.replace(hour=9, minute=0, second=0))[11:16],
#         senior_morning_end = str(now.replace(hour=12, minute=0, second=0))[11:16],
#         senior_afternoon_start = str(now.replace(hour=13, minute=0, second=0))[11:16],
#         senior_afternoon_end = str(now.replace(hour=16, minute=0, second=0))[11:16]
#         )
#     db.session.add(school)

#     for i in range(400):

#         a = Student(
#             school_id=1234,
#             id_no='2011334281',
#             first_name='Jasper',
#             last_name='Barcelona',
#             middle_name='Estrada',
#             level='2nd Grade',
#             department='student',
#             section='Charity',
#             absences='0',
#             lates='0',
#             parent_contact='09183339068'
#             )

#         b = Log(
#             school_id=1234,
#             date='1234',
#             id_no='2011334281',
#             name='Jasper',
#             level='2nd Grade',
#             department='student',
#             section='Charity',
#             time_in='0',
#             )

#         db.session.add(a)
#         db.session.add(b)

#     d = Section(
#         school_id=1234,
#         name='Charity'
#         )

#     e = Section(
#         school_id=1234,
#         name='Fidelity'
#         )

#     f = Section(
#         school_id=1234,
#         name='Peace'
#         )

#     db.session.add(d)
#     db.session.add(e)
#     db.session.add(f)
#     db.session.commit()
#     return SWJsonify({'status': 'Database Rebuild Success'})


if __name__ == '__main__':
    app.debug = True
    app.run(port=int(os.environ['PORT']), host='0.0.0.0',threaded=True)

    # port=int(os.environ['PORT']), host='0.0.0.0'
