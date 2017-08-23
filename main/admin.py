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
from flask import session, redirect
from datetime import timedelta
from datetime import datetime
from functools import wraps, update_wrapper
import threading
from threading import Timer
from multiprocessing.pool import ThreadPool
import calendar
from calendar import Calendar
from time import sleep
import requests
import datetime
from datetime import date
import time
import json
import uuid
import random
import string
import smtplib
from email.mime.text import MIMEText as text
import os
import schedule
from tasks import send_message
import db_conn
from db_conn import db, app
from models import *

API_KEY = 'ecc67d28db284a2fb351d58fe18965f9'
SCHOOL_NO = 'sgb-lc2017'
CONNECT_TIMEOUT = 5.0
CALENDAR_URL = 'http://ravenclock:5000%s'

now = datetime.datetime.now()
pool = ThreadPool(processes=1)


class IngAdmin(sqla.ModelView):
    column_display_pk = True

class SchoolAdmin(sqla.ModelView):
    column_display_pk = True
    column_include_list = ['api_key', 'name', 'url', 'address', 'city', 'email', 'tel']
    edit_template = 'test_edit.html'

class StudentAdmin(sqla.ModelView):
    column_display_pk = True
    column_searchable_list = ['first_name', 'last_name', 'middle_name', 'id_no']

admin = Admin(app, name='raven')
admin.add_view(SchoolAdmin(School, db.session))
admin.add_view(IngAdmin(Section, db.session))
admin.add_view(IngAdmin(Log, db.session))
admin.add_view(StudentAdmin(K12, db.session))
admin.add_view(IngAdmin(Parent, db.session))
admin.add_view(IngAdmin(Staff, db.session))
admin.add_view(IngAdmin(Late, db.session))
admin.add_view(IngAdmin(Absent, db.session))
admin.add_view(IngAdmin(Message, db.session))
admin.add_view(IngAdmin(Schedule, db.session))
admin.add_view(IngAdmin(Fee, db.session))
admin.add_view(IngAdmin(CollegeDepartment, db.session))
admin.add_view(IngAdmin(StaffDepartment, db.session))
admin.add_view(IngAdmin(FeeCategory, db.session))
admin.add_view(IngAdmin(StudentFee, db.session))
admin.add_view(IngAdmin(Collected, db.session))
admin.add_view(IngAdmin(FeeGroup, db.session))
admin.add_view(IngAdmin(AdminUser, db.session))
admin.add_view(IngAdmin(College, db.session))
admin.add_view(IngAdmin(Wallet, db.session))
admin.add_view(IngAdmin(Transaction, db.session))
admin.add_view(IngAdmin(TransactionItem, db.session))
admin.add_view(IngAdmin(Sale, db.session))
admin.add_view(IngAdmin(Device, db.session))
admin.add_view(IngAdmin(Permission, db.session))
admin.add_view(IngAdmin(Topup, db.session))


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
    return K12.query.filter_by(id_no=id_no).first()

def authenticate_user(email, password):
    user = AdminUser.query.filter_by(email=email,password=password).first()
    if not user or user == None:
        return jsonify(status='failed', error='Invalid email or password')
    if user.status != 'Active':
        return jsonify(status='failed', error='Your account has been deactivated')
    school = School.query.filter_by(school_no=user.school_no).first()
    session['school_no'] = school.school_no
    session['api_key'] = school.api_key
    session['school_name'] = school.name
    session['user_id'] = user.id
    session['user_school_no'] = user.school_no
    session['user_name'] = user.name
    session['department'] = 'student'
    session['tab'] = 'logs'
    return jsonify(status='success', error=''),200


def mark_morning_absent(school_no,api_key,level):
    students = K12.query.filter_by(school_no=school_no,level=level).all()

    for student in students:
        logged = Log.query.filter_by(date=time.strftime("%B %d, %Y"),id_no=student.id_no).order_by(Log.timestamp.desc()).first()
        print 'xxxxxxxxxxxxxxxxxxxxx'
        print student.id_no
        if not logged or logged == None or logged.time_out != None:
            student_name = student.last_name+', '+student.first_name
            if student.middle_name:
                student_name += ' '+student.middle_name[:1]+'.'
            absent = Absent(
            school_no=school_no,
            date=time.strftime("%B %d, %Y"),
            id_no=student.id_no,
            name=student_name,
            level=student.level,
            section=student.section,
            department=student.department,
            time_of_day='morning',
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )

            db.session.add(absent)
            student.absences=Absent.query.filter_by(id_no=student.id_no, school_no=school_no).count()
            db.session.commit()
            absent_count = Absent.query.filter_by(school_no=school_no,date=time.strftime("%B %d, %Y"),time_of_day='morning').count()
    return schedule.CancelJob


def mark_afternoon_absent(school_no,api_key):
    all_students = K12.query.filter_by(school_no=school_no).all()

    for student in all_students:
        print 'xxxxxxxxxxxxxxxxxxxxx'
        print student.id_no
        logged = Log.query.filter_by(date=time.strftime("%B %d, %Y"),id_no=student.id_no).order_by(Log.timestamp.desc()).first()
        if not logged or logged == None or logged.time_out != None:
            student_name = student.last_name+', '+student.first_name
            if student.middle_name:
                student_name += ' '+student.middle_name[:1]+'.'
            absent = Absent(
            school_no=school_no,
            date=time.strftime("%B %d, %Y"),
            id_no=student.id_no,
            name=student_name,
            level=student.level,
            section=student.section,
            department=student.department,
            time_of_day='afternoon',
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )

            db.session.add(absent)
            student.absences=Absent.query.filter_by(id_no=student.id_no, school_no=school_no).count()
            db.session.commit()
            absent_count = Absent.query.filter_by(school_no=school_no,date=time.strftime("%B %d, %Y"),time_of_day='afternoon').count()
    return jsonify(status='Success', absent_count=absent_count),201

def mark_specific_absent(school_no,id_no,time_of_day):
    student = K12.query.filter_by(school_no=school_no,id_no=id_no).first()
    student_name = student.last_name+', '+student.first_name
    if student.middle_name:
        student_name += ' '+student.middle_name[:1]+'.'
    absent = Absent(
            school_no=school_no,
            date=time.strftime("%B %d, %Y"),
            id_no=id_no,
            name=student_name,
            level=student.level,
            section=student.section,
            time_of_day=time_of_day,
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
    db.session.add(absent)
    db.session.commit()

    student.absences=Absent.query.filter_by(id_no=id_no, school_no=school_no).count()
    db.session.commit()


def check_if_late(school_no,api_key,id_no,name,level,section,date,group,time,timestamp):

    time_now = str(now.replace(hour=get_hour(time), minute=int(time[3:5])))[11:16]
    schedule = Schedule.query.filter_by(school_no=school_no).first()
    if level == 'Junior Kinder':
        educ = 'junior_kinder'
    elif level == 'Senior Kinder':
        educ = 'senior_kinder'
    elif level == '1st Grade':
        educ = 'first_grade'
    elif level == '2nd Grade':
        educ = 'second_grade'
    elif level == '3rd Grade':
        educ = 'third_grade'
    elif level == '4th Grade':
        educ = 'fourth_grade'
    elif level == '5th Grade':
        educ = 'fifth_grade'
    elif level == '6th Grade':
        educ = 'sixth_grade'
    elif level == '7th Grade':
        educ = 'seventh_grade'
    elif level == '8th Grade':
        educ = 'eight_grade'
    elif level == '9th Grade':
        educ = 'ninth_grade'
    elif level == '10th Grade':
        educ = 'tenth_grade'
    elif level == '11th Grade':
        educ = 'eleventh_grade'
    elif level == '12th Grade':
        educ = 'twelfth_grade'


    query = 'schedule.%s' %educ

    morning_class = eval(query+'_morning_class')
    afternoon_class = eval(query+'_afternoon_class')

    morning_start = eval(query+'_morning_start')
    morning_end = eval(query+'_morning_end')
    afternoon_start = eval(query+'_afternoon_start')
    afternoon_end = eval(query+'_afternoon_end')

    print 'time now: %s' % parse_date(time_now)
    print 'afternoon start: %s' % parse_date(afternoon_start)
    print 'afternoon end: %s' % parse_date(afternoon_end)
    print 'afternoon class: %s' % str(afternoon_class)

    # if ((parse_date(time_now) >= parse_date(morning_start) and parse_date(time_now) < parse_date(morning_end)) or \
    #     (parse_date(time_now) >= parse_date(afternoon_start) and parse_date(time_now) < parse_date(afternoon_end))) and\
    #     Absent.query.filter_by(school_id=school_id,id_no=id_no,date=date).first() == None:

    #     record_as_late(school_id, id_no, name, level, section, 
    #                    date, department, time)

    if parse_date(time_now) >= parse_date(morning_start) and\
        parse_date(time_now) < parse_date(morning_end) and\
        Absent.query.filter_by(school_no=school_no,id_no=id_no,date=date,time_of_day='morning').first() == None:
        if morning_class:
            if str(parse_date(time_now) - parse_date(morning_start)) > '1:00:00':
                mark_specific_absent(school_no,id_no,'morning')
            else:
                record_as_late(school_no, id_no, name, level, section, 
                            date, group, time, timestamp)

    elif (parse_date(time_now) >= parse_date(afternoon_start) and\
        parse_date(time_now) < parse_date(afternoon_end)) and\
        Absent.query.filter_by(school_no=school_no,id_no=id_no,date=date,time_of_day='afternoon').first() == None:
        if afternoon_class:
            if str(parse_date(time_now) - parse_date(afternoon_start)) > '1:00:00':
                mark_specific_absent(school_no,id_no,'afternoon')
            else:
                record_as_late(school_no, id_no, name, level, section, 
                            date, group, time, timestamp)


def record_as_late(school_no, id_no, name, level, section, 
                    date, department, time, timestamp):
    late = Late(
            school_no=school_no,date=date,id_no=id_no,
            name=name,level=level,section=section,
            time_in=time,department=department,
            timestamp=timestamp
            )

    db.session.add(late)
    db.session.commit()

    student=K12.query.filter_by(id_no=id_no, school_no=school_no).one()
    student.lates=Late.query.filter_by(id_no=id_no, school_no=school_no).count()
    db.session.commit()


def time_in(school_no,api_key,log_id,id_no,name,date,group,time,timestamp,level,section,logged):

    add_this = Log(
        school_no=school_no,
        date=date,
        id_no=id_no,
        name=name,
        group=group,
        time_in=time,
        time_in_id=log_id,
        time_in_notification_status='Pending',
        timestamp=timestamp
        )

    db.session.add(add_this)
    db.session.commit()
    if group == 'k12':
        if not logged:
            print 'sending message now'
            compose_message(add_this.id,id_no,time,'entered')
        check_if_late(school_no,api_key,id_no,name,level,section,date,group,time,timestamp)

    return jsonify(status='Success',type='entry',action='entered'), 201


def time_out(log_id, id_no, time, school_no, group):
    log = Log.query.filter_by(id_no=id_no,school_no=school_no).order_by(Log.timestamp.desc()).first()
    log.time_out = time
    log.time_out_id = log_id
    log.time_out_notification_status = 'Pending'
    db.session.commit()

    if group == 'k12':
        compose_message(log.id,id_no,time,'left')

    return jsonify(status='Success',type='exit',action='left'), 201


def compose_message(log_id,id_no,log_time,action):
    student = get_student_data(id_no)
    message = student.first_name+' '+\
              student.last_name+' has '+action+' the campus on '+ \
              time.strftime("%B %d, %Y") +' at exactly '+\
              log_time+'.'

    send_message(log_id,'log',message,student.parent_contact,action)
            
def prepare():
    global variable
    session['logs_limit']+=100
    session['late_limit']+=100
    session['attendance_limit']+=100
    variable = pool.apply_async(fetch_next, (session['logs_limit'],
                      session['late_limit'],session['attendance_limit'],
                      session['absent_limit'],session['school_no'],
                      session['department'])).get()


# def fetch_first(logs_limit, late_limit, attendance_limit, absent_limit, school_no, department):
#      logs = Log.query.filter_by(
#         school_no=school_no,
#         department=department
#         ).order_by(Log.timestamp.desc()).slice((logs_limit-100),logs_limit)

#      late = Late.query.filter_by(
#         school_no=school_no,
#         department=department
#         ).order_by(Late.timestamp.desc()).slice((late_limit-100),late_limit)

#      attendance = Student.query.filter_by(
#         school_no=school_no,
#         department=department)\
#         .order_by(Student.last_name).slice((attendance_limit-100),attendance_limit)

#      absent = Absent.query.filter_by(
#         school_no=school_no,
#         department=department)\
#         .order_by(Absent.date.desc()).slice((absent_limit-100),absent_limit)

#      return {'logs':logs, 'late':late, 'attendance':attendance, 'absent':absent}


def fetch_next(needed):
    session[needed+'_limit'] += 100

    if needed == 'logs':
        search_table = 'Log'
        template = 'logs_result.html'
        sort_by = 'timestamp'
        sort_type='.desc()'

    elif needed == 'late':
        search_table = 'Late'
        template = 'late.html'
        sort_by = 'timestamp'
        sort_type='.desc()'

    elif needed == 'k12':
        search_table = 'K12'
        sort_by = 'last_name'
        template = 'k12.html'
        sort_type=''

    if needed == 'fees':
        search_table = 'Fee'
        template = 'fees_result.html'
        sort_by = 'timestamp'
        sort_type='.desc()'


    elif needed == 'college':
        search_table = 'College'
        sort_by = 'last_name'
        template = 'college.html'
        sort_type=''

    elif needed == 'staff':
        search_table = 'Staff'
        sort_by = 'last_name'
        template = 'staff_result.html'
        sort_type=''

    elif needed == 'transactions':
        search_table = 'Transaction'
        sort_by = 'timestamp'
        template = 'transaction_result.html'
        sort_type='.desc()'

    elif needed == 'sales':
        search_table = 'Sale'
        sort_by = 'date'
        template = 'sales_result.html'
        sort_type='.desc()'

    elif needed == 'messages':
        search_table = 'Message'
        sort_by = 'timestamp'
        template = 'messages_result.html'
        sort_type='.desc()'

    elif needed == 'accounts':
        search_table = 'AdminUser'
        sort_by = 'last_name'
        template = 'accounts.html'
        sort_type=''

    elif needed == 'absent':
        search_table = 'Absent'
        sort_by = 'timestamp'
        sort_type='.desc()'
        template = 'absent.html'

    elif needed == 'topup':
        search_table = 'Topup'
        sort_by = 'timestamp'
        sort_type='.desc()'
        template = 'ewallet_result.html'

    result = eval(search_table+'.query.filter_by(school_no=session[\'school_no\']).order_by('+search_table+'.'+sort_by+sort_type+').slice('+str(session[needed+'_limit']-100)+','+str(session[needed+'_limit'])+')')
    print session['college_limit']
    return flask.render_template(
        template,
        data=result,
        limit=session[needed+'_limit']-100,
        date = time.strftime("%B %d, %Y")
        )


def search_logs(*args, **kwargs):
    query = 'Log.query.filter(Log.school_no.ilike("'+session['school_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Log.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Log.timestamp.desc()).slice(('+str(args[0])+'-100),'+str(args[0])+')'
    session['logs_search_limit']+=100
    print query
    return eval(query)

def search_transactions(*args, **kwargs):
    query = 'Transaction.query.filter(Transaction.school_no.ilike("'+session['school_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Transaction.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Transaction.timestamp.desc()).slice(('+str(args[0])+'-100),'+str(args[0])+')'
    session['logs_search_limit']+=100
    print query
    return eval(query)

def search_sales(*args, **kwargs):
    query = 'Sale.query.filter(Sale.school_no.ilike("'+session['school_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Sale.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Sale.date.desc()).slice(('+str(args[0])+'-100),'+str(args[0])+')'
    session['logs_search_limit']+=100
    print query
    return eval(query)

def search_fees(*args, **kwargs):
    query = 'Fee.query.filter(Fee.school_no.ilike("'+session['school_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Fee.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Fee.name).slice(('+str(args[0])+'-100),'+str(args[0])+')'
    session['fees_search_limit']+=100
    print query
    return eval(query)

def search_k12(*args, **kwargs):
    query = 'K12.query.filter(K12.school_no.ilike("'+session['school_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'K12.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(K12.last_name).slice(('+str(args[0])+'-100),'+str(args[0])+')'
    session['k12_search_limit']+=100
    return eval(query)

def search_college(*args, **kwargs):
    query = 'College.query.filter(College.school_no.ilike("'+session['school_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'College.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(College.last_name).slice(('+str(args[0])+'-100),'+str(args[0])+')'
    session['college_search_limit']+=100
    return eval(query)

def search_staff(*args, **kwargs):
    query = 'Staff.query.filter(Staff.school_no.ilike("'+session['school_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Staff.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Staff.last_name).slice(('+str(args[0])+'-100),'+str(args[0])+')'
    session['staff_search_limit']+=100
    return eval(query)

def search_absent(*args, **kwargs):
    query = 'Absent.query.filter(Absent.school_no.ilike("'+session['school_no']+'"),'
    for arg_name in kwargs:
        if kwargs[arg_name]:
            query += 'Absent.' + arg_name + '.ilike("%'+kwargs[arg_name]+'%"),'
    query += ').order_by(Absent.name).slice(('+str(args[0])+'-100),'+str(args[0])+')'
    session['absent_search_limit']+=100
    return eval(query)

def search_late(*args, **kwargs):
    query = 'Late.query.filter(Late.school_no.ilike("'+session['school_no']+'"),'
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
        return jsonify(status='Failed',error='School not found'),404

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
        status= 'Success',
        morning_time= morning_time,
        afternoon_time= afternoon_time
        )

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def test_job(word):
    print word

def initialize_absent(school_no,api_key):
    school = School.query.filter_by(school_no=school_no,api_key=api_key).first()
    class_schedule = Schedule.query.filter_by(school_no=school.school_no).first()

    time_format = '{:%H:%M}'

    junior_kinder_morning_start = time_format.format(parse_date(class_schedule.junior_kinder_morning_start) + timedelta(hours=1))
    senior_kinder_morning_start = time_format.format(parse_date(class_schedule.senior_kinder_morning_start) + timedelta(hours=1))
    first_grade_morning_start = time_format.format(parse_date(class_schedule.first_grade_morning_start) + timedelta(hours=1))
    second_grade_morning_start = time_format.format(parse_date(class_schedule.second_grade_morning_start) + timedelta(hours=1))
    third_grade_morning_start = time_format.format(parse_date(class_schedule.third_grade_morning_start) + timedelta(hours=1))
    fourth_grade_morning_start = time_format.format(parse_date(class_schedule.fourth_grade_morning_start) + timedelta(hours=1))
    fifth_grade_morning_start = time_format.format(parse_date(class_schedule.fifth_grade_morning_start) + timedelta(hours=1))
    sixth_grade_morning_start = time_format.format(parse_date(class_schedule.sixth_grade_morning_start) + timedelta(hours=1))
    seventh_grade_morning_start = time_format.format(parse_date(class_schedule.seventh_grade_morning_start) + timedelta(hours=1))
    eight_grade_morning_start = time_format.format(parse_date(class_schedule.eight_grade_morning_start) + timedelta(hours=1))
    ninth_grade_morning_start = time_format.format(parse_date(class_schedule.ninth_grade_morning_start) + timedelta(hours=1))
    tenth_grade_morning_start = time_format.format(parse_date(class_schedule.tenth_grade_morning_start) + timedelta(hours=1))
    eleventh_grade_morning_start = time_format.format(parse_date(class_schedule.eleventh_grade_morning_start) + timedelta(hours=1))
    twelfth_grade_morning_start = time_format.format(parse_date(class_schedule.twelfth_grade_morning_start) + timedelta(hours=1))

    print 'Junior Kinder: %s' % junior_kinder_morning_start
    print 'Junior Kinder: %s' % senior_kinder_morning_start
    print 'Junior Kinder: %s' % first_grade_morning_start
    print 'Junior Kinder: %s' % second_grade_morning_start
    print 'Junior Kinder: %s' % third_grade_morning_start
    print 'Junior Kinder: %s' % fourth_grade_morning_start
    print 'Junior Kinder: %s' % fifth_grade_morning_start
    print 'Junior Kinder: %s' % sixth_grade_morning_start
    print 'Junior Kinder: %s' % seventh_grade_morning_start
    print 'Junior Kinder: %s' % eight_grade_morning_start
    print 'Junior Kinder: %s' % ninth_grade_morning_start
    print 'Junior Kinder: %s' % tenth_grade_morning_start
    print 'Junior Kinder: %s' % eleventh_grade_morning_start
    print 'Junior Kinder: %s' % twelfth_grade_morning_start

    schedule.every().day.at(junior_kinder_morning_start).do(mark_morning_absent,school_no,api_key,'Junior Kinder')
    schedule.every().day.at(senior_kinder_morning_start).do(mark_morning_absent,school_no,api_key,'Senior Kinder')
    schedule.every().day.at(first_grade_morning_start).do(mark_morning_absent,school_no,api_key,'1st Grade')
    schedule.every().day.at(second_grade_morning_start).do(mark_morning_absent,school_no,api_key,'2nd Grade')
    schedule.every().day.at(third_grade_morning_start).do(mark_morning_absent,school_no,api_key,'3rd Grade')
    schedule.every().day.at(fourth_grade_morning_start).do(mark_morning_absent,school_no,api_key,'4th Grade')
    schedule.every().day.at(fifth_grade_morning_start).do(mark_morning_absent,school_no,api_key,'5th Grade')
    schedule.every().day.at(sixth_grade_morning_start).do(mark_morning_absent,school_no,api_key,'6th Grade')
    schedule.every().day.at(seventh_grade_morning_start).do(mark_morning_absent,school_no,api_key,'7th Grade')
    schedule.every().day.at(eight_grade_morning_start).do(mark_morning_absent,school_no,api_key,'8th Grade')
    schedule.every().day.at(ninth_grade_morning_start).do(mark_morning_absent,school_no,api_key,'9th Grade')
    schedule.every().day.at(tenth_grade_morning_start).do(mark_morning_absent,school_no,api_key,'10th Grade')
    schedule.every().day.at(eleventh_grade_morning_start).do(mark_morning_absent,school_no,api_key,'11th Grade')
    schedule.every().day.at(twelfth_grade_morning_start).do(mark_morning_absent,school_no,api_key,'12th Grade')

    while True:
        schedule.run_pending()
        time.sleep(1)
    return

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)

def send_email(new_user,email_address,user_name,school_name,password):
    # try:
    s = smtplib.SMTP('smtp.gmail.com', 587)
    myGmail = 'barcelona.jasperoliver@gmail.com'
    myGMPasswd = 'royalpsalms11'
    message = text(('Hi, %s!\r\n \r\nWelcome to Pisara! %s has added you as administrator for %s. '
               'Please go to your school\'s Pisara Dashboard URL and login with your email.\r\n \r\n'
               'Your temporary password is: %s\r\n \r\nWe strongly recommend that you change it '
               'immediately.\r\n \r\nRegards,\r\nPisara Team')%(str(new_user),str(user_name), str(school_name), str(password)))
    message['Subject'] = 'Welcome to Pisara'
    message['From'] = 'Pisara'
    message['To'] = email_address

    s.starttls()
    s.login(myGmail, myGMPasswd)
    s.sendmail(myGmail,email_address,message.as_string())
    s.quit()
    return True
    # except:
    #     return False


@app.route('/sched/get', methods=['GET', 'POST'])
def get_schedule():
    api_key = flask.request.args.get('api_key')
    return get_latest_schedule(api_key)


@app.route('/', methods=['GET', 'POST'])
@nocache
def dashboard():
    if not session:
        return redirect('/login')
    session['logs_limit'] = 0
    session['late_limit'] = 0
    session['k12_limit'] = 0
    session['college_limit'] = 0
    session['staff_limit'] = 0
    session['absent_limit'] = 0
    session['fees_limit'] = 0
    session['transactions_limit'] = 0
    session['sales_limit'] = 0
    session['topup_limit'] = 0
    session['messages_limit'] = 0
    session['accounts_limit'] = 0

    session['logs_search_limit'] = 0
    session['fees_search_limit'] = 0
    session['k12_search_limit'] = 0
    session['late_search_limit'] = 0
    session['absent_search_limit'] = 0
    session['staff_search_limit'] = 0
    session['transactions_search_limit'] = 0
    session['sales_search_limit'] = 0
    session['topup_search_limit'] = 0
    session['messages_search_limit'] = 0
    session['accounts_search_limit'] = 0

    session['k12_search_status'] = False
    session['college_search_status'] = False
    session['absent_search_status'] = False
    session['late_search_status'] = False
    session['logs_search_status'] = False
    session['staff_search_status'] = False
    session['fees_search_status'] = False
    session['transactions_search_status'] = False
    session['sales_search_status'] = False
    session['topup_search_status'] = False
    session['messages_search_status'] = False
    session['accounts_search_status'] = False

    school = School.query.filter_by(api_key=session['api_key']).first()
    sections = Section.query.filter_by(school_no=school.school_no).order_by(Section.name).all()
    departments = Department.query.filter_by(school_no=school.school_no).order_by(Department.name).all()
    fee_categories = FeeCategory.query.order_by(FeeCategory.name).all()
    fees = Fee.query.filter_by(school_no=session['school_no']).order_by(Fee.name).all()
    college_departments = CollegeDepartment.query.filter_by(school_no=school.school_no).order_by(CollegeDepartment.name).all()
    staff_departments = StaffDepartment.query.filter_by(school_no=school.school_no).order_by(StaffDepartment.name).all()
    user = AdminUser.query.filter_by(id=session['user_id']).first()
    modules = Module.query.all()

    # prepare()

    return flask.render_template(
        'index.html',
        user_name=session['user_name'],
        user = user,
        sections=sections,
        fees=fees,
        fee_categories=fee_categories,
        college_departments=college_departments,
        staff_departments=staff_departments,
        departments=departments,
        modules=modules,
        school_name=session['school_name']
        )


@app.route('/students', methods=['GET', 'POST'])
@nocache
def students():
    session['k12_limit']=0
    session['college_limit']=0
    session['k12_limit']+=100
    session['college_limit']+=100
    school = School.query.filter_by(api_key=session['api_key']).first()
    k12 = K12.query.order_by(K12.last_name).slice((session['k12_limit']-100),session['k12_limit'])
    college = College.query.order_by(College.last_name).slice((session['college_limit']-100),session['college_limit'])
    college_departments = CollegeDepartment.query.filter_by(school_no=school.school_no).order_by(CollegeDepartment.name).all()
    sections = Section.query.filter_by(school_no=school.school_no).order_by(Section.name).all()
    return flask.render_template(
        'students.html',
        k12=k12,
        college=college,
        sections=sections,
        college_departments=college_departments,
        k12_limit=session['k12_limit'],
        college_limit=session['college_limit']
        )


@app.route('/students/fees/add', methods=['GET', 'POST'])
@nocache
def add_student_fee():
    student = K12.query.filter_by(id=session['student_id']).first()
    fees_to_add = flask.request.form.getlist('fees_to_add[]')
    student_name = student.last_name+', '+student.first_name
    if student.middle_name:
        student_name += ' '+student.middle_name[:1]+'.'
    print 'xxxxxxxxxxxxxxx'
    print fees_to_add
    for fee in fees_to_add:
        fee = Fee.query.filter_by(id=fee).first()
        student_fee = StudentFee(
            school_no = session['school_no'],
            student_id = student.id,
            fee_id = fee.id,
            student_name = student_name,
            fee_name = fee.name,
            fee_category = fee.category,
            fee_price = fee.price,
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
        db.session.add(student_fee)
        db.session.commit()

    student_fees = StudentFee.query.filter_by(student_id=student.id).order_by(StudentFee.fee_name).all()
    total_fees = sum(fee.fee_price for fee in student_fees)
    collected_payments = Collected.query.filter_by(student_id=student.id).order_by(Collected.timestamp).all()
    total_paid = sum(payment.amount for payment in collected_payments)
    return flask.render_template(
        'student_fees.html',
        student=student,
        student_fees=student_fees,
        total_fees=total_fees,
        collected_payments=collected_payments,
        total_paid=total_paid
        )


@app.route('/staff', methods=['GET', 'POST'])
@nocache
def staff():
    session['staff_limit']=0
    session['staff_limit']+=100
    school = School.query.filter_by(api_key=session['api_key']).first()
    staff = Staff.query.order_by(Staff.last_name).slice((session['staff_limit']-100),session['staff_limit'])
    staff_departments = StaffDepartment.query.filter_by(school_no=school.school_no).order_by(StaffDepartment.name).all()
    return flask.render_template(
        'staff.html',
        staff=staff,
        staff_departments=staff_departments,
        staff_limit=session['staff_limit']
        )


@app.route('/logs', methods=['GET', 'POST'])
@nocache
def logs():
    session['logs_limit']=0
    session['logs_limit']+=100
    logs = Log.query.order_by(Log.timestamp.desc()).slice((session['logs_limit']-100),session['logs_limit'])
    return flask.render_template(
        'logs.html',
        logs=logs,
        logs_limit=session['logs_limit']
        )


@app.route('/celery/test',methods=['GET','POST'])
def test_celery():
    add.delay(5, 5)
    return 'ok'


@app.route('/messages',methods=['GET','POST'])
@nocache
def messages():
    session['messages_limit']=0
    session['messages_limit']+=100
    messages = Message.query.order_by(Message.timestamp.desc()).slice((session['messages_limit']-100),session['messages_limit'])
    return flask.render_template(
        'messages.html',
        messages=messages,
        messages_limit=session['messages_limit']
        )

    
@app.route('/topup/student/get', methods=['GET', 'POST'])
@nocache
def get_topup_student():
    id_no = flask.request.form.get('wallet_no')
    student = K12.query.filter_by(id_no=id_no).first()
    if not student:
        return jsonify(
            status='failed',
            message='Invalid ID'
            )
    session['topup_student_id'] = student.id_no
    wallet = Wallet.query.filter_by(student_id=student.id).first()
    student_name = student.last_name+', '+student.first_name
    if student.middle_name:
        student_name += ' '+student.middle_name[:1]+'.'
    return jsonify(
        status='success',
        template=flask.render_template('wallet_info.html',student=student, student_name=student_name, wallet=wallet)
        )


@app.route('/topup', methods=['GET', 'POST'])
@nocache
def topup():
    amount = flask.request.form.get('amount')
    student = K12.query.filter_by(id_no=session['topup_student_id']).first()

    wallet = Wallet.query.filter_by(student_id=student.id).first()
    wallet.credits = wallet.credits + float(amount)
    db.session.commit()

    student_name = student.last_name+', '+student.first_name
    if student.middle_name:
        student_name += ' '+student.middle_name[:1]+'.'

    new_topup = Topup(
        school_no = session['school_no'],
        date = datetime.datetime.now().strftime('%B %d, %Y'),
        time = time.strftime("%I:%M %p"),
        student_id = student.id,
        student_name = student_name,
        id_no = student.id_no,
        amount = amount,
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )
    db.session.add(new_topup)
    db.session.commit()

    wallets = Wallet.query.filter_by(school_no=session['school_no']).all()
    available_credits = sum(wallet.credits for wallet in wallets)

    session['topup_limit'] = 0
    session['topup_limit'] += 100
    data = Topup.query.order_by(Topup.timestamp.desc()).slice((session['topup_limit']-100),session['topup_limit'])
    return jsonify(
        template=flask.render_template('ewallet_result.html',data=data,limit=session['topup_limit']),
        available_credits=available_credits
        )


@app.route('/wallet', methods=['GET', 'POST'])
@nocache
def wallet():
    session['wallet_limit']=0
    session['wallet_limit']+=100
    topups = Topup.query.order_by(Topup.timestamp.desc()).slice((session['wallet_limit']-100),session['wallet_limit'])
    wallets = Wallet.query.filter_by(school_no=session['school_no']).all()
    available_credits = sum(wallet.credits for wallet in wallets)
    return flask.render_template(
        'ewallet.html',
        topups=topups,
        wallet_limit=session['wallet_limit'],
        available_credits=available_credits
        )


@app.route('/transactions', methods=['GET', 'POST'])
@nocache
def transactions():
    session['transactions_limit']=0
    session['sales_limit']=0
    session['transactions_limit']+=100
    session['sales_limit']+=100
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).slice((session['transactions_limit']-100),session['transactions_limit'])
    sales = Sale.query.order_by(Sale.date.desc()).slice((session['sales_limit']-100),session['sales_limit'])
    devices = Device.query.filter_by(device_type='POS').all()
    return flask.render_template(
        'transactions.html',
        transactions=transactions,
        transactions_limit=session['transactions_limit'],
        sales=sales,
        sales_limit=session['sales_limit'],
        date = time.strftime("%B %d, %Y"),
        devices = devices
        )


@app.route('/attendance', methods=['GET', 'POST'])
@nocache
def attendance():
    session['absent_limit']=0
    session['late_limit']=0
    session['absent_limit']+=100
    session['late_limit']+=100
    absent = Absent.query.order_by(Absent.timestamp.desc()).slice((session['absent_limit']-100),session['absent_limit'])
    late = Late.query.order_by(Late.timestamp.desc()).slice((session['late_limit']-100),session['late_limit'])
    return flask.render_template(
        'attendance.html',
        absent=absent,
        late=late,
        attendance_limit=session['absent_limit'],
        late_limit=session['late_limit']
        )


@app.route('/fees', methods=['GET', 'POST'])
@nocache
def fees():
    session['fees_limit']=0
    session['fees_limit']+=100
    fees = Fee.query.order_by(Fee.name).all()
    fee_categories = FeeCategory.query.order_by(FeeCategory.name).all()
    return flask.render_template('fees.html',fees=fees, fee_categories=fee_categories)


@app.route('/fees/new', methods=['GET', 'POST'])
@nocache
def save_new_fee():
    data = flask.request.form.to_dict()
    if data.get('desc'):
        new_fee = Fee(
            school_no=session['school_no'],
            name=data['name'],
            category=data['category'],
            price=data['price'],
            desc=data['desc'],
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
    else:
        new_fee = Fee(
            school_no=session['school_no'],
            name=data['name'],
            category=data['category'],
            price=data['price'],
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
    db.session.add(new_fee)
    db.session.commit()

    add_to = flask.request.form.getlist('add_to[]')
    if add_to != []:
        for level in add_to:
            fee_group = FeeGroup(
                school_no=session['school_no'],
                fee_id=new_fee.id,
                level=level
                )
            db.session.add(fee_group)
            db.session.commit()

        fees_thread = threading.Thread(target=add_fees,args=[session['school_no'],add_to,new_fee.id])
        fees_thread.start()

    session['fees_limit'] = 0;
    session['fees_search_limit'] = 0;
    return fetch_next('fees')

def add_fees(school_no,add_to,fee_id):
    fee = Fee.query.filter_by(id=fee_id).first()
    for level in add_to:
        students = K12.query.filter_by(level=level).all()
        for student in students:
            student_name = student.last_name+', '+student.first_name
            if student.middle_name:
                student_name += ' '+student.middle_name[:1]+'.'
            new_student_fee = StudentFee(
                school_no = school_no,
                student_id = student.id,
                student_name = student_name,
                fee_id = fee.id,
                fee_name = fee.name,
                fee_category = fee.category,
                fee_price = fee.price,
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                )
            db.session.add(new_student_fee)
            db.session.commit()
    return


@app.route('/attendance/reset', methods=['GET', 'POST'])
def reset_attendance():
    students = K12.query.all()
    for student in students:
        student.absences = 0
        student.lates = 0
    db.session.commit()
    return jsonify(status='Success'),200

65
@app.route('/accounts', methods=['GET', 'POST'])
def manage_accounts():
    session['accounts_limit']=0
    session['accounts_limit']+=100
    accounts = AdminUser.query.order_by(AdminUser.name).slice((session['accounts_limit']-100),session['accounts_limit'])
    return flask.render_template(
        'accounts.html',
        accounts=accounts,
        accounts_limit=session['accounts_limit']
        )


@app.route('/account/new', methods=['GET', 'POST'])
def new_account():
    account_info = flask.request.form.to_dict()
    email_account = AdminUser.query.filter_by(email=account_info['account_email']).first()

    if email_account or email_account != None:
        return jsonify(status='failed',error='Email already in use')

    temp_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))

    if send_email(account_info['account_name'].title(),account_info['account_email'],session['user_name'],session['school_name'], temp_password):
        new_account = AdminUser(
            school_no=session['school_no'],
            email=account_info['account_email'],
            password=temp_password,
            name=account_info['account_name'].title(),
            added_by=session['user_id'],\
            join_date=datetime.datetime.now().strftime('%B %d, %Y'),
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f'),
            students_access=account_info['students_access'],
            staff_access=account_info['staff_access'],
            logs_access=account_info['logs_access'],
            attendance_access=account_info['attendance_access'],
            wallet_access=account_info['wallet_access'],
            fees_access=account_info['fees_access'],
            transactions_access=account_info['transactions_access'],
            accounts_access=account_info['accounts_access'],
            broadcast_access=account_info['broadcast_access'],
            schedule_access=account_info['schedule_access'],
            calendar_access=account_info['calendar_access'],
            new_id_access=account_info['new_id_access']
            )

        db.session.add(new_account)
        db.session.commit()

        accounts = AdminUser.query.order_by(AdminUser.name).slice((session['accounts_limit']-100),session['accounts_limit'])
        return jsonify(status='success',template=flask.render_template('account_table.html',accounts=accounts))
    return jsonify(status='failed',error='Could not connect to server.')


@app.route('/schedule/irregular/get', methods=['GET', 'POST'])
def get_irregular_schedule():
    data = flask.request.form.to_dict()
    session['day'] = data['day']
    calendar_params = {
        'api_key':session['api_key'],
        'month':data['month'],
        'day':data['day'],
        'year':data['year']
    }
    get_events = requests.get(CALENDAR_URL%'/schedule/irregular/get',params=calendar_params)
    schedule = get_events.json()
    return jsonify(
        date=str(calendar.month_name[int(data['month'])]+' ' +data['day']+', '+data['year']),
        junior_kinder_morning_class=schedule['junior_kinder_morning_class'],
        junior_kinder_afternoon_class=schedule['junior_kinder_afternoon_class'],
        senior_kinder_morning_class=schedule['senior_kinder_morning_class'],
        senior_kinder_afternoon_class=schedule['senior_kinder_afternoon_class'],
        first_grade_morning_class=schedule['first_grade_morning_class'],
        first_grade_afternoon_class=schedule['first_grade_afternoon_class'],
        second_grade_morning_class=schedule['second_grade_morning_class'],
        second_grade_afternoon_class=schedule['second_grade_afternoon_class'],
        third_grade_morning_class=schedule['third_grade_morning_class'],
        third_grade_afternoon_class=schedule['third_grade_afternoon_class'],
        fourth_grade_morning_class=schedule['fourth_grade_morning_class'],
        fourth_grade_afternoon_class=schedule['fourth_grade_afternoon_class'],
        fifth_grade_morning_class=schedule['fifth_grade_morning_class'],
        fifth_grade_afternoon_class=schedule['fifth_grade_afternoon_class'],
        sixth_grade_morning_class=schedule['sixth_grade_morning_class'],
        sixth_grade_afternoon_class=schedule['sixth_grade_afternoon_class'],
        seventh_grade_morning_class=schedule['seventh_grade_morning_class'],
        seventh_grade_afternoon_class=schedule['seventh_grade_afternoon_class'],
        eight_grade_morning_class=schedule['eight_grade_morning_class'],
        eight_grade_afternoon_class=schedule['eight_grade_afternoon_class'],
        ninth_grade_morning_class=schedule['ninth_grade_morning_class'],
        ninth_grade_afternoon_class=schedule['ninth_grade_afternoon_class'],
        tenth_grade_morning_class=schedule['tenth_grade_morning_class'],
        tenth_grade_afternoon_class=schedule['tenth_grade_afternoon_class'],
        eleventh_grade_morning_class=schedule['eleventh_grade_morning_class'],
        eleventh_grade_afternoon_class=schedule['eleventh_grade_afternoon_class'],
        twelfth_grade_morning_class=schedule['twelfth_grade_morning_class'],
        twelfth_grade_afternoon_class=schedule['twelfth_grade_afternoon_class'],
        junior_kinder_morning_start=schedule['junior_kinder_morning_start'],
        junior_kinder_morning_end=schedule['junior_kinder_morning_end'],
        junior_kinder_afternoon_start=schedule['junior_kinder_afternoon_start'],
        junior_kinder_afternoon_end=schedule['junior_kinder_afternoon_end'],
        senior_kinder_morning_start=schedule['senior_kinder_morning_start'],
        senior_kinder_morning_end=schedule['senior_kinder_morning_end'],
        senior_kinder_afternoon_start=schedule['senior_kinder_afternoon_start'],
        senior_kinder_afternoon_end=schedule['senior_kinder_afternoon_end'],
        first_grade_morning_start=schedule['first_grade_morning_start'],
        first_grade_morning_end=schedule['first_grade_morning_end'],
        first_grade_afternoon_start=schedule['first_grade_afternoon_start'],
        first_grade_afternoon_end=schedule['first_grade_afternoon_end'],
        second_grade_morning_start=schedule['second_grade_morning_start'],
        second_grade_morning_end=schedule['second_grade_morning_end'],
        second_grade_afternoon_start=schedule['second_grade_afternoon_start'],
        second_grade_afternoon_end=schedule['second_grade_afternoon_end'],
        third_grade_morning_start=schedule['third_grade_morning_start'],
        third_grade_morning_end=schedule['third_grade_morning_end'],
        third_grade_afternoon_start=schedule['third_grade_afternoon_start'],
        third_grade_afternoon_end=schedule['third_grade_afternoon_end'],
        fourth_grade_morning_start=schedule['fourth_grade_morning_start'],
        fourth_grade_morning_end=schedule['fourth_grade_morning_end'],
        fourth_grade_afternoon_start=schedule['fourth_grade_afternoon_start'],
        fourth_grade_afternoon_end=schedule['fourth_grade_afternoon_end'],
        fifth_grade_morning_start=schedule['fifth_grade_morning_start'],
        fifth_grade_morning_end=schedule['fifth_grade_morning_end'],
        fifth_grade_afternoon_start=schedule['fifth_grade_afternoon_start'],
        fifth_grade_afternoon_end=schedule['fifth_grade_afternoon_end'],
        sixth_grade_morning_start=schedule['sixth_grade_morning_start'],
        sixth_grade_morning_end=schedule['sixth_grade_morning_end'],
        sixth_grade_afternoon_start=schedule['sixth_grade_afternoon_start'],
        sixth_grade_afternoon_end=schedule['sixth_grade_afternoon_end'],
        seventh_grade_morning_start=schedule['seventh_grade_morning_start'],
        seventh_grade_morning_end=schedule['seventh_grade_morning_end'],
        seventh_grade_afternoon_start=schedule['seventh_grade_afternoon_start'],
        seventh_grade_afternoon_end=schedule['seventh_grade_afternoon_end'],
        eight_grade_morning_start=schedule['eight_grade_morning_start'],
        eight_grade_morning_end=schedule['eight_grade_morning_end'],
        eight_grade_afternoon_start=schedule['eight_grade_afternoon_start'],
        eight_grade_afternoon_end=schedule['eight_grade_afternoon_end'],
        ninth_grade_morning_start=schedule['ninth_grade_morning_start'],
        ninth_grade_morning_end=schedule['ninth_grade_morning_end'],
        ninth_grade_afternoon_start=schedule['ninth_grade_afternoon_start'],
        ninth_grade_afternoon_end=schedule['ninth_grade_afternoon_end'],
        tenth_grade_morning_start=schedule['tenth_grade_morning_start'],
        tenth_grade_morning_end=schedule['tenth_grade_morning_end'],
        tenth_grade_afternoon_start=schedule['tenth_grade_afternoon_start'],
        tenth_grade_afternoon_end=schedule['tenth_grade_afternoon_end'],
        eleventh_grade_morning_start=schedule['eleventh_grade_morning_start'],
        eleventh_grade_morning_end=schedule['eleventh_grade_morning_end'],
        eleventh_grade_afternoon_start=schedule['eleventh_grade_afternoon_start'],
        eleventh_grade_afternoon_end=schedule['eleventh_grade_afternoon_end'],
        twelfth_grade_morning_start=schedule['twelfth_grade_morning_start'],
        twelfth_grade_morning_end=schedule['twelfth_grade_morning_end'],
        twelfth_grade_afternoon_start=schedule['twelfth_grade_afternoon_start'],
        twelfth_grade_afternoon_end=schedule['twelfth_grade_afternoon_end']
        )


@app.route('/login', methods=['GET', 'POST'])
@nocache
def login_page():
    if session:
        return redirect('/')
    return flask.render_template('login.html')


@app.route('/user/authenticate', methods=['GET', 'POST'])
def login():
    if session:
        return redirect('/')
    login_data = flask.request.form.to_dict()
    return authenticate_user(login_data['user_email'], login_data['user_password'])


@app.route('/home', methods=['GET', 'POST'])
def start_again():
    needed = flask.request.form.get('tab') 
    session[needed+'_search_status'] = False
    session[needed+'_limit'] = 0
    session[needed+'_search_limit'] = 100
    return fetch_next(needed)


@app.route('/loadmore', methods=['GET', 'POST'])
def load_more():
    needed = flask.request.form.get('data')
    return fetch_next(needed)


@app.route('/view', methods=['GET', 'POST'])
def change_view():
    view = flask.request.args.get('view')
    session['department'] = view
    return redirect('/')


@app.route('/absent/morning/mark', methods=['GET', 'POST'])
def mark_absent_morning():
    school_no = flask.request.form.get('school_no')
    api_key = flask.request.form.get('api_key')

    if not api_key or not School.query.filter_by(school_no=school_no, api_key=api_key):
        return jsonify(status='Failed', error='School not found'),404

    return mark_morning_absent(school_no,api_key)


@app.route('/absent/afternoon/mark', methods=['GET', 'POST'])
def mark_absent_afternoon():
    school_no = flask.request.form.get('school_no')
    api_key = flask.request.form.get('api_key')

    if not api_key or not School.query.filter_by(school_no=school_no, api_key=api_key):
        return jsonify(status='Failed',error='School not found'),404

    return mark_afternoon_absent(school_no,api_key)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/login')


def retry_sms(unsent_sms):
    for sms in unsent_sms:
        if sms.time_out == '' or sms.time_out == None or sms.time_out == 'None':
            action = 'entered'
            time = sms.time_in
        else:
            action = 'left'
            time = sms.time_out
        print 'xxxxxxxxxxxxxxxxxxxxxxx'
        print 'retrying' + str(sms.id_no)
        compose_message(sms.id,sms.id_no,time,action)
    return 'success',200


@app.route('/sms/retry', methods=['GET', 'POST'])
def sms_retry():
    unsent_sms = Log.query.filter_by(date=time.strftime("%B %d, %Y"),notification_status='Failed').all()
    retry_sms_thread = threading.Thread(target=retry_sms,args=[unsent_sms])
    retry_sms_thread.start()
    return jsonify(status='success'),200
        


@app.route('/student/info/get', methods=['GET', 'POST'])
def get_student_info():
    student_id = flask.request.form.get('student_id')
    session['student_id'] = student_id
    student = K12.query.filter_by(id=student_id).first()
    guardian = Parent.query.filter_by(id=student.parent_id).first()
    sections = Section.query.filter_by(school_no=session['school_no']).all()
    departments = Department.query.filter_by(school_no=session['school_no']).all()
    student_fees = StudentFee.query.filter_by(student_id=student.id).order_by(StudentFee.fee_name).all()
    total_fees = sum(fee.fee_price for fee in student_fees)
    collected_payments = Collected.query.filter_by(student_id=student.id).order_by(Collected.timestamp).all()
    total_paid = sum(payment.amount for payment in collected_payments)
    return flask.render_template(
            'student_info.html',
            student=student,
            guardian=guardian,
            sections=sections,
            departments=departments,
            student_fees=student_fees,
            total_fees=total_fees,
            collected_payments=collected_payments,
            total_paid=total_paid
            )


@app.route('/fees/collect', methods=['GET', 'POST'])
def collect_fees():
    student = K12.query.filter_by(id=session['student_id']).first()
    amount = flask.request.form.get('amount')
    collection = Collected(
        school_no=session['school_no'],
        student_id=session['student_id'],
        amount=amount,
        date=time.strftime("%B %d, %Y"),
        time=time.strftime("%I:%M %p"),
        timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )
    db.session.add(collection)
    db.session.commit()

    student_fees = StudentFee.query.filter_by(student_id=session['student_id']).order_by(StudentFee.fee_name).all()
    total_fees = sum(fee.fee_price for fee in student_fees)
    collected_payments = Collected.query.filter_by(student_id=session['student_id']).order_by(Collected.timestamp).all()
    total_paid = sum(payment.amount for payment in collected_payments)

    return flask.render_template(
        'student_fees.html',
        student=student,
        student_fees=student_fees,
        total_fees=total_fees,
        collected_payments=collected_payments,
        total_paid=total_paid
        )


@app.route('/college/info/get', methods=['GET', 'POST'])
def get_college_info():
    student_id = flask.request.form.get('student_id')
    student = College.query.filter_by(id=student_id).first()
    departments = CollegeDepartment.query.filter_by(school_no=session['school_no']).all()
    return flask.render_template('college_info.html', student=student, college_departments=departments)


@app.route('/staff/info/get', methods=['GET', 'POST'])
def get_staff_info():
    staff_id = flask.request.form.get('staff_id')
    staff = Staff.query.filter_by(id=staff_id).first()
    departments = StaffDepartment.query.filter_by(school_no=session['school_no']).all()
    return flask.render_template('staff_info.html', staff=staff, staff_departments=departments)


@app.route('/tab/change', methods=['GET', 'POST'])
def change_tab():
    tab = flask.request.form.get('tab')
    session['tab'] = tab
    return '',200


@app.route('/addlog', methods=['POST'])
def add_log():
    data = flask.request.form.to_dict()

    if not data['api_key'] or not School.query.filter_by(school_no=data['school_no'],api_key=data['api_key']):
        return jsonify(status='500',message='Unauthorized'), 500

    logged = Log.query.filter_by(date=data['date'],school_no=data['school_no'],id_no=data['id_no']).order_by(Log.timestamp.desc()).first()

    if not logged or logged.time_out != None:

        return time_in(data['school_no'],data['api_key'],data['log_id'],data['id_no'],data['name'],
               data['date'],data['group'],data['time'],data['timestamp'],data['level'],data['section'],
               logged)

    return time_out(data['log_id'],data['id_no'],data['time'],data['school_no'],data['group'])    


@app.route('/messages/new',methods=['GET','POST'])
def blast_message():
    recipients = flask.request.form.getlist('recipients[]')
    message = flask.request.form.get('message')

    msisdn = []

    if 'Parents' in recipients:
        for user in db.session.query(K12.parent_contact).distinct():
            msisdn.append(user)

    if 'College' in recipients:
        for user in db.session.query(College.mobile).distinct():
            msisdn.append(user)

    if 'Staff' in recipients:
        for user in db.session.query(Staff.mobile).distinct():
            msisdn.append(user)

    # ADD SMS CODE HERE

    new_message = Message(
        school_no = session['school_no'],
        sender_id = session['user_id'],
        sender_name = session['user_name'],
        recipient = ", ".join(recipients),
        date = datetime.datetime.now().strftime('%B %d, %Y'),
        time = time.strftime("%I:%M %p"),
        content = message,
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    db.session.add(new_message)
    db.session.commit()

    session['messages_limit'] = 0
    session['messages_search_limit'] = 0

    return fetch_next('messages')


@app.route('/sync',methods=['GET','POST'])
def sync_database():
    school_no = flask.request.args.get('school_no')
    return SWJsonify({
        'k12': K12.query.filter_by(school_no=school_no).all(),
        'college': College.query.filter_by(school_no=school_no).all(),
        'staff': Staff.query.filter_by(school_no=school_no).all()
        }), 201


@app.route('/data/receive',methods=['GET','POST'])
def receive_records():
    data = flask.request.form.to_dict()
    if K12.query.filter_by(id_no=data['id_no']).first() or K12.query.filter_by(id_no=data['id_no']).first() != None:
        return jsonify(status='success'),201

    if data.get('middle_name'):
        student = Student(
        school_no='123456789',
        id_no=data['id_no'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        middle_name=data['middle_name'],
        level=data['level'],
        department=data['department'],
        section=data['section'],
        absences=0,
        lates=0,
        parent_contact=data['parent_contact']
        )
    else:
        student = Student(
        school_no='123456789',
        id_no=data['id_no'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        level=data['level'],
        department=data['department'],
        section=data['section'],
        absences=0,
        lates=0,
        parent_contact=data['parent_contact']
        )
    db.session.add(student)
    db.session.commit()
    return jsonify(status='success'),201


@app.route('/guardians/info',methods=['GET','POST'])
def get_guardian_info():
    mobile_number = flask.request.form.get('mobile_number')
    guardian = Parent.query.filter_by(mobile_number=mobile_number).first()
    if guardian or guardian != None:
        return jsonify(
            status='success',
            last_name=guardian.last_name,
            first_name=guardian.first_name,
            middle_name=guardian.middle_name,
            email=guardian.email,
            address=guardian.address,
            ),200
    return jsonify(
        status='failed',
        message='not found'
        )


@app.route('/user/new',methods=['GET','POST'])
def add_user():
    student_data = flask.request.form.to_dict()
    if student_data['department'] == 'k12':
        guardian = Parent.query.filter_by(mobile_number=student_data['guardian_mobile']).first()
        if guardian or guardian != None:
            parent_id = guardian.id
        else:
            new_guardian = Parent(
                school_no = session['school_no'],
                mobile_number = student_data['guardian_mobile'],
                last_name = student_data['guardian_last_name'].title(),
                first_name = student_data['guardian_first_name'].title(),
                middle_name = student_data['guardian_middle_name'].title(),
                email = student_data['guardian_email'],
                address = student_data['guardian_address'].title()
                )
            db.session.add(new_guardian)
            db.session.commit()

        guardian = Parent.query.filter_by(mobile_number=student_data['guardian_mobile']).first()
        parent_id = guardian.id

        user = K12(
            school_no = session['school_no'],
            id_no = student_data['id_no'],
            first_name = student_data['first_name'].title(),
            last_name = student_data['last_name'].title(),
            middle_name = student_data['middle_name'].title(),
            level = student_data['level'],
            section = student_data['section'].title(),
            group = 'k12',
            absences = 0,
            lates = 0,
            parent_id = parent_id,
            parent_relation = student_data['guardian_relation'].title(),
            parent_contact = student_data['guardian_mobile'],
            added_by = session['user_name']
            )

        db.session.add(user)
        db.session.commit()

        student_name = user.last_name+', '+user.first_name
        if user.middle_name:
            student_name += ' '+user.middle_name[:1]+'.'

        fees_to_add = FeeGroup.query.filter_by(level=user.level).all()
        if fees_to_add != None:
            for item in fees_to_add:
                fee = Fee.query.filter_by(id=item.fee_id).first()
                new_student_fee = StudentFee(
                    school_no = session['school_no'],
                    student_id = user.id,
                    student_name = student_name,
                    fee_id = fee.id,
                    fee_name = fee.name,
                    fee_category = fee.category,
                    fee_price = fee.price,
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                    )

                db.session.add(new_student_fee)
                db.session.commit()

        wallet = Wallet(
            school_no=session['school_no'],
            student_id=user.id,
            student_name=student_name,
            id_no=user.id_no
            )
        db.session.add(wallet)
        db.session.commit()

    elif student_data['department'] == 'college':
        user = College(
            school_no = session['school_no'],
            id_no = student_data['id_no'],
            first_name = student_data['first_name'].title(),
            last_name = student_data['last_name'].title(),
            middle_name = student_data['middle_name'].title(),
            level = student_data['level'],
            department = student_data['college_department'],
            email = student_data['email'],
            mobile = student_data['mobile'],
            group = 'college',
            added_by = session['user_name']
            )

        db.session.add(user)
        db.session.commit()

    elif student_data['department'] == 'staff':
        user = Staff(
            school_no = session['school_no'],
            id_no = student_data['id_no'],
            first_name = student_data['first_name'].title(),
            last_name = student_data['last_name'].title(),
            middle_name = student_data['middle_name'].title(),
            department = student_data['staff_department'],
            email = student_data['email'],
            mobile = student_data['mobile'],
            group = 'staff',
            added_by = session['user_name']
            )

        db.session.add(user)
        db.session.commit()

    session[student_data['department']+'_limit'] = 0
    
    session[student_data['department']+'_search_limit'] = 0

    return fetch_next(student_data['department'])

    # prepare()


@app.route('/student/edit',methods=['GET','POST'])
def edit_user():

    data = flask.request.form.to_dict()

    user = K12.query.filter_by(id=data['user_id']).first()
    user.last_name = data['last_name']
    user.first_name = data['first_name']
    user.middle_name = data['middle_name']
    user.level = data['level']
    user.section = data['section']
    user.id_no = data['id_no']

    db.session.commit()

    parent = Parent.query.filter_by(mobile_number=data['guardian_mobile']).first()
    if parent or parent != None:
        parent.first_name = data['guardian_first_name']
        parent.last_name = data['guardian_last_name']
        parent.middle_name = data['guardian_middle_name']
        parent.email = data['guardian_email']
        parent.address = data['guardian_address']
        user.parent_id = parent.id

    else:
        new_parent = Parent(
            mobile_number = data['guardian_mobile'],
            first_name = data['guardian_first_name'],
            last_name = data['guardian_first_name'],
            middle_name = data['guardian_first_name'],
            email = data['guardian_email'],
            address = data['guardian_address']
            )
        db.session.add(new_parent)
        db.session.commit()
        parent = Parent.query.filter_by(mobile_number=data['guardian_mobile']).first()
        user.parent_id = parent.id
        user.parent_contact = parent.mobile_number

    user.parent_relation = data['guardian_relation']
    db.session.commit()

    session['k12_limit'] = 0
    
    session['k12_search_limit'] = 0

    if session['k12_search_status']:
        result = search_k12(session['k12_search_limit'],last_name=session['attendance_data']['last_name'], first_name=session['attendance_data']['first_name'],
                middle_name=session['attendance_data']['middle_name'], id_no=session['attendance_data']['id_no'], level=session['attendance_data']['level'], section=session['attendance_data']['section'])
        return flask.render_template(
        session['attendance_data']['needed']+'.html',
        data=result,
        view=session['department'],
        limit=session['k12_search_limit']-100
        )

    return fetch_next('k12')


@app.route('/college/edit',methods=['GET','POST'])
def edit_college():

    data = flask.request.form.to_dict()

    user = College.query.filter_by(id=data['user_id']).first()
    user.last_name = data['last_name']
    user.first_name = data['first_name']
    user.middle_name = data['middle_name']
    user.level = data['level']
    user.department = data['college_department']
    user.email = data['email']
    user.mobile = data['contact']
    user.id_no = data['id_no']

    db.session.commit()

    
    session['college_limit'] = 0
    
    session['college_search_limit'] = 0

    if session['college_search_status']:
        result = search_college(session['college_search_limit'],last_name=session['college_data']['last_name'], first_name=session['college_data']['first_name'],
                middle_name=session['college_data']['middle_name'], id_no=session['college_data']['id_no'], level=session['college_data']['level'], department=session['college_data']['department'])
        return flask.render_template(
        session['college_data']['needed']+'.html',
        data=result,
        limit=session['college_search_limit']-100
        )

    return fetch_next('college')


@app.route('/staff/edit',methods=['GET','POST'])
def edit_staff():

    data = flask.request.form.to_dict()

    user = Staff.query.filter_by(id=data['user_id']).first()
    user.last_name = data['last_name']
    user.first_name = data['first_name']
    user.middle_name = data['middle_name']
    user.department = data['staff_department']
    user.email = data['email']
    user.mobile = data['contact']
    user.id_no = data['id_no']

    db.session.commit()

    
    session['staff_limit'] = 0
    
    session['staff_search_limit'] = 0

    if session['staff_search_status']:
        result = search_staff(session['staff_search_limit'],last_name=session['staff_data']['last_name'], first_name=session['staff_data']['first_name'],
                middle_name=session['staff_data']['middle_name'], id_no=session['staff_data']['id_no'], department=session['staff_data']['department'])
        return flask.render_template(
        'staff_result.html',
        data=result,
        limit=session['staff_search_limit']-100
        )

    return fetch_next('staff')


@app.route('/search/logs',methods=['GET','POST'])
def search_student_logs():
    session['logs_data'] = flask.request.form.to_dict()
    session['logs_search_status'] = True

    if session['logs_data']['reset'] == 'yes':
        session['logs_search_limit']=0
    
    limit = session['logs_search_limit']

    result = search_logs(session['logs_search_limit'],date=session['logs_data']['date'], id_no=session['logs_data']['id_no'],
                       name=session['logs_data']['name'], group=session['logs_data']['department'])
    
    return flask.render_template(
        'logs_result.html',
        data=result,
        limit=limit
        )


@app.route('/search/transactions',methods=['GET','POST'])
def search_school_transactions():
    session['transactions_data'] = flask.request.form.to_dict()
    session['transactions_search_status'] = True

    if session['transactions_data']['reset'] == 'yes':
        session['transactions_search_limit']=0
    
    limit = session['transactions_search_limit']

    result = search_transactions(session['transactions_search_limit'],date=session['transactions_data']['date'], time=session['transactions_data']['time'], customer_id_no=session['transactions_data']['id_no'],
                       customer_name=session['transactions_data']['customer_name'], transaction_type=session['transactions_data']['transaction_type'], vendor_name=session['transactions_data']['vendor_name'])
    
    return flask.render_template(
        'transaction_result.html',
        data=result,
        limit=limit
        )


@app.route('/search/sales',methods=['GET','POST'])
def search_school_sales():
    session['sales_data'] = flask.request.form.to_dict()
    session['sales_search_status'] = True

    if session['sales_data']['reset'] == 'yes':
        session['sales_search_limit']=0
    
    limit = session['sales_search_limit']

    result = search_sales(session['sales_search_limit'],date=session['sales_data']['date'], vendor=session['sales_data']['vendor_name'])
    
    return flask.render_template(
        'sales_result.html',
        data=result,
        limit=limit
        )


@app.route('/search/fees',methods=['GET','POST'])
def search_student_fees():
    session['fees_data'] = flask.request.form.to_dict()
    session['fees_search_status'] = True

    if session['fees_data']['reset'] == 'yes':
        session['fees_search_limit'] = 0
    
    limit = session['fees_search_limit']

    result = search_fees(session['fees_search_limit'],name=session['fees_data']['name'], category=session['fees_data']['category'])
    print 'xxxxxxxxxxxxxxxxxxxxx'
    print result 
    return flask.render_template(
        'fees_result.html',
        data=result,
        limit=limit
        )


@app.route('/search/k12',methods=['GET','POST'])
def search_students_k12():
    session['attendance_data'] = flask.request.form.to_dict()
    session['k12_search_status'] = True

    if session['attendance_data']['reset'] == 'yes':
        session['k12_search_limit'] = 0
    
    limit = session['k12_search_limit']

    result = search_k12(session['k12_search_limit'],last_name=session['attendance_data']['last_name'], first_name=session['attendance_data']['first_name'],
            middle_name=session['attendance_data']['middle_name'], level=session['attendance_data']['level'], section=session['attendance_data']['section'], id_no=session['attendance_data']['id_no'])


    return flask.render_template(
        session['attendance_data']['needed']+'.html',
        data=result,
        limit=limit
        )


@app.route('/search/college',methods=['GET','POST'])
def search_students_college():
    session['college_data'] = flask.request.form.to_dict()
    session['college_search_status'] = True

    if session['college_data']['reset'] == 'yes':
        session['college_search_limit'] = 0
    
    limit = session['college_search_limit']

    result = search_college(session['college_search_limit'],last_name=session['college_data']['last_name'], first_name=session['college_data']['first_name'],
            middle_name=session['college_data']['middle_name'], level=session['college_data']['level'], department=session['college_data']['department'], id_no=session['college_data']['id_no'])


    return flask.render_template(
        session['college_data']['needed']+'.html',
        data=result,
        limit=limit
        )


@app.route('/search/staff',methods=['GET','POST'])
def search_user_staff():
    session['staff_data'] = flask.request.form.to_dict()
    session['staff_search_status'] = True

    if session['staff_data']['reset'] == 'yes':
        session['staff_search_limit'] = 0
    
    limit = session['staff_search_limit']

    result = search_staff(session['staff_search_limit'],last_name=session['staff_data']['last_name'], first_name=session['staff_data']['first_name'],
            middle_name=session['staff_data']['middle_name'], department=session['staff_data']['department'], id_no=session['staff_data']['id_no'])


    return flask.render_template(
        'staff_result.html',
        data=result,
        limit=limit
        )



@app.route('/search/absent',methods=['GET','POST'])
def search_student_absent():
    data = flask.request.form.to_dict()

    if data['reset'] == 'yes':
        session['absent_search_limit']=100
    
    limit = session['absent_search_limit']-100
    
    result = search_absent(session['absent_search_limit'], date=data['date'], id_no=data['id_no'],
                       name=data['name'], level=data['level'],
                       section=data['section'])

    return flask.render_template(
        data['needed']+'.html',
        data=result,
        view=session['department'],
        limit=limit
        )


@app.route('/search/late',methods=['GET','POST'])
def search_student_late():
    data = flask.request.form.to_dict()

    if data['reset'] == 'yes':
        session['late_search_limit']=100
    
    limit = session['late_search_limit']-100
    
    result = search_late(session['late_search_limit'], date=data['date'], id_no=data['id_no'],
                       name=data['name'], level=data['level'],
                       section=data['section'])

    return flask.render_template(
        data['needed']+'.html',
        data=result,
        view=session['department'],
        limit=limit
        )


@app.route('/schedule/regular/save',methods=['GET','POST'])
def change_sched():
    schedule = flask.request.form.getlist('schedule[]')

    sched_data = {
        'api_key': session['api_key'],
        'schedule': schedule 
    }

    try:
        r = requests.post(CALENDAR_URL%'/schedule/regular/update',sched_data)
        print r.status_code #update log database (put 'sent' to status)

    except requests.exceptions.ConnectionError as e:
        print "Disconnected!"

    return '',200


@app.route('/schedule/irregular/save',methods=['GET','POST'])
def change_irregular_sched():
    schedule = flask.request.form.to_dict()

    request_param = {
        'api_key':session['api_key'],
        'month':session['month'],
        'day':session['day'],
        'year':session['year']
    }

    try:
        r = requests.post(CALENDAR_URL%'/schedule/irregular/new',schedule,params=request_param)
        print r.status_code #update log database (put 'sent' to status)

    except requests.exceptions.ConnectionError as e:
        print "Disconnected!"

    return '',200


@app.route('/id/validate',methods=['GET','POST'])
def validate_id():
    id_no = flask.request.form.get('id_no')
    k12 = K12.query.filter_by(id_no=id_no).first()
    college = College.query.filter_by(id_no=id_no).first()
    staff = Staff.query.filter_by(id_no=id_no).first()
    if k12 == None and college == None and staff == None:
        return ''
    else:
        return 'Duplicate ID Number'


@app.route('/id/validate/edit',methods=['GET','POST'])
def validate_id_edit():
    id_no = flask.request.form.get('id_no')
    group = flask.request.form.get('group')
    student_id = flask.request.form.get('student_id')
    k12 = K12.query.filter_by(id=student_id,group=group).first()
    college = College.query.filter_by(id=student_id,group=group).first()
    k12_id_no = K12.query.filter_by(id_no=id_no).first()
    college_id_no = College.query.filter_by(id_no=id_no).first()
    if k12_id_no != None or college_id_no != None:
        if k12 != None:
            if k12.id_no != id_no:
                return 'Duplicate ID Number'
            else:
                return ''
        elif college != None:
            if college.id_no != id_no:
                return 'Duplicate ID Number'
            else:
                return ''
    else:
        return ''


@app.route('/calendar/data/get',methods=['GET','POST'])
def populate_calendar():
    cal = Calendar(6)
    session['year'] = date.today().year
    session['month'] = date.today().month
    day = date.today().day
    dates = cal.monthdatescalendar(session['year'], session['month'])

    calendar_params = {
        'api_key':session['api_key'],
        'month':session['month'],
        'year':session['year']
    }

    try:
        get_events = requests.get(CALENDAR_URL%'/events/get',params=calendar_params)
        events = get_events.json()['days']
        return flask.render_template('dates.html', dates=dates, year=session['year'], month=session['month'], today=day, events=events, month_name=calendar.month_name[session['month']])

    except requests.exceptions.ConnectionError as e:
        return flask.render_template('dates.html', dates=dates, year=session['year'], month=session['month'], month_name=calendar.month_name[session['month']], today=day) #return diff template??


@app.route('/calendar/date/go',methods=['GET','POST'])
def next_month():
    data = flask.request.form.to_dict()
    cal = Calendar(6)
    session['month'] = int(data['month'])
    session['year'] = int(data['year'])
    dates = cal.monthdatescalendar(session['year'], session['month'])

    calendar_params = {
        'api_key':session['api_key'],
        'month':session['month'],
        'year':session['year']
    }

    try:
        get_events = requests.get(CALENDAR_URL%'/events/get',params=calendar_params)
        events = get_events.json()['days']
        return flask.render_template('dates.html', dates=dates, year=session['year'], month=session['month'], today='', events=events, month_name=calendar.month_name[session['month']])

    except requests.exceptions.ConnectionError as e:
        return flask.render_template('dates.html', dates=dates, year=session['year'], month=session['month'], today='')


@app.route('/calendar/prev/get',methods=['GET','POST'])
def prev_month():
    cal = Calendar(6)
    if session['month'] == 1:
        session['year'] -= 1
        session['month'] = 12
    else:
        session['month'] -= 1
    dates = cal.monthdatescalendar(session['year'], session['month'])

    calendar_params = {
        'api_key':session['api_key'],
        'month':session['month'],
        'year':session['year']
    }

    try:
        get_events = requests.get(CALENDAR_URL%'/events/get',params=calendar_params)
        events = get_events.json()['days']
        return flask.render_template('dates.html', dates=dates, year=session['year'], month=session['month'], today='', events=events, month_name=calendar.month_name[session['month']])

    except requests.exceptions.ConnectionError as e:
        return flask.render_template('dates.html', dates=dates, year=session['year'], month=session['month'], today='')


@app.route('/schedule/regular/get',methods=['GET','POST'])
def populate_regular_schedule():
    calendar_params = {
        'api_key':session['api_key']
    }

    try:
        get_sched = requests.get(CALENDAR_URL%'/schedule/regular/get',params=calendar_params)
        return SWJsonify({
        'monday': get_sched.json()['monday'],
        'tuesday': get_sched.json()['tuesday'],
        'wednesday': get_sched.json()['wednesday'],
        'thursday': get_sched.json()['thursday'],
        'friday': get_sched.json()['friday'],
        }), 200

    except requests.exceptions.ConnectionError as e:
        return flask.render_template('dates.html', dates=dates, year=session['year'], month=session['month'], month_name=calendar.month_name[session['month']], today='')


@app.route('/schedule/sync',methods=['GET','POST'])
def sync_schedule():
    data = flask.request.form.to_dict()

    schedule = Schedule.query.filter_by(school_no=data['school_no']).one()

    schedule.junior_kinder_morning_class = str2bool(data['junior_kinder_morning_class'])
    schedule.junior_kinder_afternoon_class = str2bool(data['junior_kinder_afternoon_class'])
    schedule.senior_kinder_morning_class = str2bool(data['senior_kinder_morning_class'])
    schedule.senior_kinder_afternoon_class = str2bool(data['senior_kinder_afternoon_class'])
    schedule.first_grade_morning_class = str2bool(data['first_grade_morning_class'])
    schedule.first_grade_afternoon_class = str2bool(data['first_grade_afternoon_class'])
    schedule.second_grade_morning_class = str2bool(data['second_grade_morning_class'])
    schedule.second_grade_afternoon_class = str2bool(data['second_grade_afternoon_class'])
    schedule.third_grade_morning_class = str2bool(data['third_grade_morning_class'])
    schedule.third_grade_afternoon_class = str2bool(data['third_grade_afternoon_class'])
    schedule.fourth_grade_morning_class = str2bool(data['fourth_grade_morning_class'])
    schedule.fourth_grade_afternoon_class = str2bool(data['fourth_grade_afternoon_class'])
    schedule.fifth_grade_morning_class = str2bool(data['fifth_grade_morning_class'])
    schedule.fifth_grade_afternoon_class = str2bool(data['fifth_grade_afternoon_class'])
    schedule.sixth_grade_morning_class = str2bool(data['sixth_grade_morning_class'])
    schedule.sixth_grade_afternoon_class = str2bool(data['sixth_grade_afternoon_class'])
    schedule.seventh_grade_morning_class = str2bool(data['seventh_grade_morning_class'])
    schedule.seventh_grade_afternoon_class = str2bool(data['seventh_grade_afternoon_class'])
    schedule.eight_grade_morning_class = str2bool(data['eight_grade_morning_class'])
    schedule.eight_grade_afternoon_class = str2bool(data['eight_grade_afternoon_class'])
    schedule.ninth_grade_morning_class = str2bool(data['ninth_grade_morning_class'])
    schedule.ninth_grade_afternoon_class = str2bool(data['ninth_grade_afternoon_class'])
    schedule.tenth_grade_morning_class = str2bool(data['tenth_grade_morning_class'])
    schedule.tenth_grade_afternoon_class = str2bool(data['tenth_grade_afternoon_class'])
    schedule.eleventh_grade_morning_class = str2bool(data['eleventh_grade_morning_class'])
    schedule.eleventh_grade_afternoon_class = str2bool(data['eleventh_grade_afternoon_class'])
    schedule.twelfth_grade_morning_class = str2bool(data['twelfth_grade_morning_class'])
    schedule.twelfth_grade_afternoon_class = str2bool(data['twelfth_grade_afternoon_class'])

    schedule.junior_kinder_morning_start = data['junior_kinder_morning_start']
    schedule.junior_kinder_morning_end = data['junior_kinder_morning_end']
    schedule.junior_kinder_afternoon_start = data['junior_kinder_afternoon_start']
    schedule.junior_kinder_afternoon_end = data['junior_kinder_afternoon_end']
    schedule.senior_kinder_morning_start = data['senior_kinder_morning_start']
    schedule.senior_kinder_morning_end = data['senior_kinder_morning_end']
    schedule.senior_kinder_afternoon_start = data['senior_kinder_afternoon_start']
    schedule.senior_kinder_afternoon_end = data['senior_kinder_afternoon_end']
    schedule.first_grade_morning_start = data['first_grade_morning_start']
    schedule.first_grade_morning_end = data['first_grade_morning_end']
    schedule.first_grade_afternoon_start = data['first_grade_afternoon_start']
    schedule.first_grade_afternoon_end = data['first_grade_afternoon_end']
    schedule.second_grade_morning_start = data['second_grade_morning_start']
    schedule.second_grade_morning_end = data['second_grade_morning_end']
    schedule.second_grade_afternoon_start = data['second_grade_afternoon_start']
    schedule.second_grade_afternoon_end = data['second_grade_afternoon_end']
    schedule.third_grade_morning_start = data['third_grade_morning_start']
    schedule.third_grade_morning_end = data['third_grade_morning_end']
    schedule.third_grade_afternoon_start = data['third_grade_afternoon_start']
    schedule.third_grade_afternoon_end = data['third_grade_afternoon_end']
    schedule.fourth_grade_morning_start = data['fourth_grade_morning_start']
    schedule.fourth_grade_morning_end = data['fourth_grade_morning_end']
    schedule.fourth_grade_afternoon_start = data['fourth_grade_afternoon_start']
    schedule.fourth_grade_afternoon_end = data['fourth_grade_afternoon_end']
    schedule.fifth_grade_morning_start = data['fifth_grade_morning_start']
    schedule.fifth_grade_morning_end = data['fifth_grade_morning_end']
    schedule.fifth_grade_afternoon_start = data['fifth_grade_afternoon_start']
    schedule.fifth_grade_afternoon_end = data['fifth_grade_afternoon_end']
    schedule.sixth_grade_morning_start = data['sixth_grade_morning_start']
    schedule.sixth_grade_morning_end = data['sixth_grade_morning_end']
    schedule.sixth_grade_afternoon_start = data['sixth_grade_afternoon_start']
    schedule.sixth_grade_afternoon_end = data['sixth_grade_afternoon_end']
    schedule.seventh_grade_morning_start = data['seventh_grade_morning_start']
    schedule.seventh_grade_morning_end = data['seventh_grade_morning_end']
    schedule.seventh_grade_afternoon_start = data['seventh_grade_afternoon_start']
    schedule.seventh_grade_afternoon_end = data['seventh_grade_afternoon_end']
    schedule.eight_grade_morning_start = data['eight_grade_morning_start']
    schedule.eight_grade_morning_end = data['eight_grade_morning_end']
    schedule.eight_grade_afternoon_start = data['eight_grade_afternoon_start']
    schedule.eight_grade_afternoon_end = data['eight_grade_afternoon_end']
    schedule.ninth_grade_morning_start = data['ninth_grade_morning_start']
    schedule.ninth_grade_morning_end = data['ninth_grade_morning_end']
    schedule.ninth_grade_afternoon_start = data['ninth_grade_afternoon_start']
    schedule.ninth_grade_afternoon_end = data['ninth_grade_afternoon_end']
    schedule.tenth_grade_morning_start = data['tenth_grade_morning_start']
    schedule.tenth_grade_morning_end = data['tenth_grade_morning_end']
    schedule.tenth_grade_afternoon_start = data['tenth_grade_afternoon_start']
    schedule.tenth_grade_afternoon_end = data['tenth_grade_afternoon_end']
    schedule.eleventh_grade_morning_start = data['eleventh_grade_morning_start']
    schedule.eleventh_grade_morning_end = data['eleventh_grade_morning_end']
    schedule.eleventh_grade_afternoon_start = data['eleventh_grade_afternoon_start']
    schedule.eleventh_grade_afternoon_end = data['eleventh_grade_afternoon_end']
    schedule.twelfth_grade_morning_start = data['twelfth_grade_morning_start']
    schedule.twelfth_grade_morning_end = data['twelfth_grade_morning_end']
    schedule.twelfth_grade_afternoon_start = data['twelfth_grade_afternoon_start']
    schedule.twelfth_grade_afternoon_end = data['twelfth_grade_afternoon_end']

    db.session.commit()

    # INITIALIZE PYSCHEDULER HERE
    absent_thread = threading.Thread(target=initialize_absent,args=[data['school_no'],data['api_key']])
    absent_thread.start()
    return '',201


@app.route('/favicon.ico',methods=['GET','POST'])
def favicon():
    return '',200


@app.route('/wallet/info',methods=['GET','POST'])
def get_wallet():
    app_key = flask.request.args.get('app_key') 
    id_no = flask.request.args.get('id_no')

    ### ADD IP_ADDRESS TO QUERY
    if not app_key or Device.query.filter_by(app_key=app_key).first() == None:
        return jsonify(status='failed',message='Unauthorized'),401

    wallet = Wallet.query.filter_by(id_no=id_no).first()
    if not wallet:
        return jsonify(status='failed',message='Invalid ID'),404

    return jsonify(
        status='success',
        student_name=wallet.student_name,
        credits=wallet.credits
        ),200


@app.route('/transaction/save',methods=['GET','POST'])
def save_pos_transaction():
    params = flask.request.args.to_dict()
    data = flask.request.form.to_dict()

    ### ADD IP_ADDRESS TO QUERY
    if not params['app_key'] or Device.query.filter_by(app_key=params['app_key']).first() == None:
        return jsonify(status='failed',message='Unauthorized'),401

    device = Device.query.filter_by(app_key=params['app_key']).first()

    sale = Sale.query.filter_by(date=time.strftime("%B %d, %Y"),vendor=device.vendor).first()
    if not sale or sale == None:
        sale = Sale(
        school_no=SCHOOL_NO,
        date=time.strftime("%B %d, %Y"),
        vendor=device.vendor,
        cash_total=0,
        wallet_total=0,
        grand_total=0
        )
        db.session.add(sale)
        db.session.commit()

    if data['transaction_type'] == 'Cash':
        transaction = Transaction(
        id = data['transaction_id'],
        school_no = data['school_no'],
        date = datetime.datetime.strptime(data['date'], '%m / %d / %Y').strftime('%B %d, %Y'),
        time = data['time'],
        vendor_id = device.id,
        vendor_name = device.vendor,
        cashier_id = data['cashier_id'],
        cashier_name = data['cashier_name'],
        total = data['total'],
        amount_tendered = data['amount_tendered'],
        change = data['change'],
        payed = 1,
        timestamp = data['timestamp'],
        transaction_type = data['transaction_type']
        )

        sale.cash_total += data['total']

    else:
        transaction = Transaction(
            id = data['transaction_id'],
            school_no = data['school_no'],
            date = datetime.datetime.strptime(data['date'], '%m / %d / %Y').strftime('%B %d, %Y'),
            time = data['time'],
            vendor_id = device.id,
            vendor_name = device.vendor,
            cashier_id = data['cashier_id'],
            cashier_name = data['cashier_name'],
            customer_name = data['customer_name'],
            customer_id_no = data['customer_id_no'],
            total = data['total'],
            payed = 1,
            timestamp = data['timestamp'],
            transaction_type = data['transaction_type']
            )

        sale.wallet_total += float(data['total'])

    sale.grand_total += float(data['total'])
    db.session.add(transaction)
    db.session.commit()

    for item in data['items']:
        transaction_item = TransactionItem(
            transaction_id = int(item['transaction_id']),
            item_id = item['item_id'],
            item_name = item['item_name'],
            item_qty = item['item_qty'],
            price = item['price'],
            flavor_id = item['flavor_id'],
            done = False
        )
        db.session.add(transaction_item)
    db.session.commit()

    return '',201


@app.route('/messages/view',methods=['GET','POST'])
def view_sent_messages():
    message_id = flask.request.form.get('message_id')
    message = Message.query.filter_by(id=message_id).first()
    return flask.render_template('message.html',message=message)


@app.route('/db/faculty/add', methods=['GET', 'POST'])
def add_faculty():
    for i in range(500):
        a = Student(
            school_no=1234,
            id_no=str(i),
            first_name='Jasper'+str(i),
            last_name='Barcelona',
            middle_name='Estrada',
            department='faculty',
            parent_contact='639183339068'
            )
        db.session.add(a)
        db.session.commit()
    return 'done'


@app.route('/db/school/add', methods=['GET', 'POST'])
def add_school():
    school = School(
        id=1234,
        api_key='ecc67d28db284a2fb351d58fe18965f3',
        password='test',
        name="Scuola Gesu Bambino",
        address="10, Brgy Isabang",
        city="Lucena City",
        email="sgb.edu@gmail.com",
        tel="555-8898",

        kinder_morning_start = str(now.replace(hour=7, minute=0, second=0))[11:16],
        kinder_morning_end = str(now.replace(hour=12, minute=0, second=0))[11:16],
        kinder_afternoon_start = str(now.replace(hour=13, minute=0, second=0))[11:16],
        kinder_afternoon_end = str(now.replace(hour=18, minute=0, second=0))[11:16],

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
    db.session.commit()
    return 'okay'


@app.route('/db/rebuild', methods=['GET', 'POST'])
def rebuild_database():
    db.drop_all()
    db.create_all()

    k12 = K12(
        school_no = 'sgb-lc2017',
        id_no = '2011334281',
        first_name = 'Jasper Oliver',
        last_name = 'Barcelona',
        middle_name = 'Estrada',
        level = '1st Grade',
        group = 'k12',
        section = 'St. Jerome',
        parent_id = 1,
        parent_relation = 'mother',
        parent_contact = '09183339068',
        added_by = 'Jasper Barcelona'
        )

    parent = Parent(
        school_no = 'sgb-lc2017',
        mobile_number = '09183339068',
        first_name = 'Flora',
        last_name = 'Barcelona',
        middle_name = 'Estrada',
        email = 'barcelona.jasperoliver@gmail.com',
        address = 'Lucena City'
        )

    wallet = Wallet(
        school_no = 'sgb-lc2017',
        student_id = 1,
        student_name = 'Barcelona, Jasper Oliver E.',
        id_no = '2011334281'
        )

    admin = AdminUser(
        school_no = 'sgb-lc2017',
        email = 'admin@gmail.com',
        password = 'ratmaxi8',
        name = 'Super User',
        status = 'Active',
        students_access = 'View, Edit, and Delete',
        staff_access = 'View, Edit, and Delete',
        logs_access = 'View, Edit, and Delete',
        attendance_access = 'View, Edit, and Delete',
        wallet_access = 'View, Edit, and Delete',
        fees_access = 'View, Edit, and Delete',
        transactions_access = 'View, Edit, and Delete',
        accounts_access = 'View, Edit, and Delete',
        broadcast_access = 'View, Edit, and Delete',
        schedule_access = 'View, Edit, and Delete',
        calendar_access = 'View, Edit, and Delete',
        new_id_access = 'View, Edit, and Delete',
        timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        )

    school = School(
        school_no='sgb-lc2017',
        api_key='ecc67d28db284a2fb351d58fe18965f9',
        name="Scuola Gesu Bambino",
        address="Barcelona Compound, Brgy Isabang",
        city="Lucena",
        email="sgb@gmail.com",
        contact="555-4079"
        )

    schedule = Schedule(
        school_no='sgb-lc2017',
        junior_kinder_morning_class=False,
        junior_kinder_afternoon_class=False,
        senior_kinder_morning_class=False,
        senior_kinder_afternoon_class=False,
        first_grade_morning_class=False,
        first_grade_afternoon_class=False,
        second_grade_morning_class=False,
        second_grade_afternoon_class=False,
        third_grade_morning_class=False,
        third_grade_afternoon_class=False,
        fourth_grade_morning_class=False,
        fourth_grade_afternoon_class=False,
        fifth_grade_morning_class=False,
        fifth_grade_afternoon_class=False,
        sixth_grade_morning_class=False,
        sixth_grade_afternoon_class=False,
        seventh_grade_morning_class=False,
        seventh_grade_afternoon_class=False,
        eight_grade_morning_class=False,
        eight_grade_afternoon_class=False,
        ninth_grade_morning_class=False,
        ninth_grade_afternoon_class=False,
        tenth_grade_morning_class=False,
        tenth_grade_afternoon_class=False,
        eleventh_grade_morning_class=False,
        eleventh_grade_afternoon_class=False,
        twelfth_grade_morning_class=False,
        twelfth_grade_afternoon_class=False,

        junior_kinder_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        junior_kinder_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        junior_kinder_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        junior_kinder_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        senior_kinder_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        senior_kinder_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        senior_kinder_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        senior_kinder_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        first_grade_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        first_grade_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        first_grade_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        first_grade_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        second_grade_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        second_grade_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        second_grade_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        second_grade_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        third_grade_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        third_grade_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        third_grade_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        third_grade_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        fourth_grade_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        fourth_grade_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        fourth_grade_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        fourth_grade_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        fifth_grade_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        fifth_grade_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        fifth_grade_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        fifth_grade_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        sixth_grade_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        sixth_grade_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        sixth_grade_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        sixth_grade_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        seventh_grade_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        seventh_grade_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        seventh_grade_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        seventh_grade_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        eight_grade_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        eight_grade_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        eight_grade_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        eight_grade_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        ninth_grade_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        ninth_grade_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        ninth_grade_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        ninth_grade_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        tenth_grade_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        tenth_grade_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        tenth_grade_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        tenth_grade_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        eleventh_grade_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        eleventh_grade_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        eleventh_grade_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        eleventh_grade_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        twelfth_grade_morning_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        twelfth_grade_morning_end=str(now.replace(hour=8, minute=0, second=0))[11:16],
        twelfth_grade_afternoon_start=str(now.replace(hour=8, minute=0, second=0))[11:16],
        twelfth_grade_afternoon_end=str(now.replace(hour=8, minute=0, second=0))[11:16]
        )
    db.session.add(school)
    db.session.add(schedule)
    db.session.add(admin)
    db.session.commit()

    d = Section(
        school_no='sgb-lc2017',
        name='Benedict'
        )

    e = Section(
        school_no='sgb-lc2017',
        name='Anthony'
        )

    f = Section(
        school_no='sgb-lc2017',
        name='Ignatius'
        )

    g = Section(
        school_no='sgb-lc2017',
        name='Louis'
        )

    h = Section(
        school_no='sgb-lc2017',
        name='John'
        )

    i = Section(
        school_no='sgb-lc2017',
        name='Francis'
        )

    j = Section(
        school_no='sgb-lc2017',
        name='Lorenzo Ruiz'
        )

    k = Section(
        school_no='sgb-lc2017',
        name='Augustine'
        )

    l = Section(
        school_no='sgb-lc2017',
        name='Vincent'
        )

    m = Section(
        school_no='sgb-lc2017',
        name='Thomas'
        )

    n = Section(
        school_no='sgb-lc2017',
        name='Jerome'
        )

    o = Department(
        school_no='sgb-lc2017',
        name='Faculty'
        )

    p = Department(
        school_no='sgb-lc2017',
        name='Maintenance'
        )

    q = Department(
        school_no='sgb-lc2017',
        name='Guidance'
        )

    r = Department(
        school_no='sgb-lc2017',
        name='Student Affairs'
        )

    s = CollegeDepartment(
        school_no='sgb-lc2017',
        name='CFAD'
        )

    t = CollegeDepartment(
        school_no='sgb-lc2017',
        name='IABF'
        )

    module = Module(
        name = 'students'
        )

    module1 = Module(
        name = 'staff'
        )

    module2 = Module(
        name = 'logs'
        )

    module3 = Module(
        name = 'attendance'
        )

    module4 = Module(
        name = 'wallet'
        )

    module5 = Module(
        name = 'fees'
        )

    module6 = Module(
        name = 'transactions'
        )

    module7 = Module(
        name = 'accounts'
        )

    module8 = Module(
        name = 'broadcast'
        )

    module9 = Module(
        name = 'schedule'
        )

    module10 = Module(
        name = 'calendar'
        )

    module11 = Module(
        name = 'new_id'
        )

    vendor = Device(
        school_no = 'sgb-lc2017',
        app_key = '4tqgtah47riyk9475lbmho6847dyth6o',
        name = 'Canteen POS Main',
        device_type = 'POS',
        vendor = 'Canteen',
        added_by = 'Jasper Barcelona'
        )

    db.session.add(d)
    db.session.add(e)
    db.session.add(f)
    db.session.add(g)
    db.session.add(h)
    db.session.add(i)
    db.session.add(j)
    db.session.add(k)
    db.session.add(l)
    db.session.add(m)
    db.session.add(n)
    db.session.add(o)
    db.session.add(p)
    db.session.add(q)
    db.session.add(r)
    db.session.add(s)
    db.session.add(t)
    db.session.add(vendor)
    db.session.add(k12)
    db.session.add(parent)
    db.session.add(wallet)

    db.session.add(module)
    db.session.add(module1)
    db.session.add(module2)
    db.session.add(module3)
    db.session.add(module4)
    db.session.add(module5)
    db.session.add(module6)
    db.session.add(module7)
    db.session.add(module8)
    db.session.add(module9)
    db.session.add(module10)
    db.session.add(module11)

    db.session.commit()

    return jsonify(status='Success'),201


@app.route('/cloud/students', methods=['GET', 'POST'])
def temporary_sync():
    r = requests.post('http://projectraven.herokuapp.com/temporary/sync')
    students = r.json()['students']

    for student in students:
        print 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
        print 'Saving %s...' % student['id_no']
        if 'parent_contact' in student:
            new_parent = Parent(
                school_no='sgb-lc2017',
                mobile_number=student['parent_contact']
                )
        else:
            new_parent = Parent(
                school_no='sgb-lc2017',
                )
        db.session.add(new_parent)
        db.session.commit()
        if 'middle_name' in student:
            if 'parent_contact' in student:
                new_student = K12(  
                    school_no = 'sgb-lc2017',
                    id_no = student['id_no'],
                    first_name = student['first_name'],
                    last_name = student['last_name'],
                    middle_name = student['middle_name'],
                    level = student['level'],
                    group = 'k12',
                    section = student['section'],
                    parent_contact = student['parent_contact'],
                    parent_id = new_parent.id
                )
            else:
                new_student = K12(  
                    school_no = 'sgb-lc2017',
                    id_no = student['id_no'],
                    first_name = student['first_name'],
                    last_name = student['last_name'],
                    middle_name = student['middle_name'],
                    level = student['level'],
                    group = 'k12',
                    section = student['section'],
                    parent_id = new_parent.id
                )
        else:
            if 'parent_contact' in student:
                new_student = K12(  
                    school_no = 'sgb-lc2017',
                    id_no = student['id_no'],
                    first_name = student['first_name'],
                    last_name = student['last_name'],
                    level = student['level'],
                    group = 'k12',
                    section = student['section'],
                    parent_contact = student['parent_contact'],
                    parent_id = new_parent.id
                )
            else:
                new_student = K12(  
                    school_no = 'sgb-lc2017',
                    id_no = student['id_no'],
                    first_name = student['first_name'],
                    last_name = student['last_name'],
                    level = student['level'],
                    group = 'k12',
                    section = student['section'],
                    parent_id = new_parent.id
                )
        db.session.add(new_student)
        db.session.commit()

    return jsonify(
        status='success'
        ),201

if __name__ == '__main__':
    app.run(port=5000,debug=True,host='0.0.0.0')
    # port=int(os.environ['PORT']), host='0.0.0.0'
