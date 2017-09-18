from celery import Celery
import db_conn
from db_conn import db
from models import *
import requests
import uuid
from xhtml2pdf import pisa
from cStringIO import StringIO
from dateutil.parser import parse as parse_date
import datetime
import time
from time import sleep
from flask import jsonify

app = Celery('tasks', broker='amqp://sgb:sgbsaints@rabbitmq/pisara')

IPP_URL = 'https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/21586853/requests'
PASSPHRASE = 'PF5H8S9t7u'
APP_ID = 'MEoztReRyeHzaiXxaecR65HnqE98tz9g'
APP_SECRET = '01c5d1f8d3bfa9966786065c5a2d829d7e84cf26fbfb4a47c91552cb7c091608'

# os.environ['DATABASE_URL']
# 'postgresql://admin:sgbsaints@db/sgb'
# 'sqlite:///local.db'

@app.task
def blast_sms(batch_id,date,time,message_content):
    batch = Message.query.filter_by(id=batch_id).first()

    messages = MessageStatus.query.filter_by(message_id=batch_id).all()
    for message in messages:

        message_options = {
            'app_id': APP_ID,
            'app_secret': APP_SECRET,
            'message': message_content,
            'address': message.msisdn,
            'passphrase': PASSPHRASE,
        }

        try:
            r = requests.post(IPP_URL,message_options)           
            if r.status_code == 201:
                message.status = 'success'
                message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                db.session.commit()

            elif r.json()['error'] == 'Invalid address.':
                message.status = 'Invalid address'
                message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                db.session.commit()

            else:
                message.status = 'Failed'
                message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                db.session.commit()

        except requests.exceptions.ConnectionError as e:
            message.status = 'Failed'
            message.timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            db.session.commit()
        
        batch.done = MessageStatus.query.filter_by(message_id=batch.id,status='success').count()
        batch.pending = MessageStatus.query.filter_by(message_id=batch.id,status='pending').count()
        batch.failed = MessageStatus.query.filter_by(message_id=batch.id,status='failed').count()
        db.session.commit()

    return


def send_absent_message(absent_id,message,msisdn):
    absent = Absent.query.filter_by(id=absent_id).first()

    message_options = {
            'app_id': APP_ID,
            'app_secret': APP_SECRET,
            'message': message,
            'address': msisdn,
            'passphrase': PASSPHRASE,
        }

    try:
        r = requests.post(IPP_URL,message_options)           
        if r.status_code == 201:
            absent.notification_status='Success'
            db.session.commit()
            return

        if r.json()['error'] == 'Invalid address.':
            absent.notification_status='Invalid address'
            db.session.commit()
            return

        absent.notification_status='Failed'
        db.session.commit()
        return

    except requests.exceptions.ConnectionError as e:
        absent.notification_status='Failed'
        db.session.commit()
        return

@app.task
def send_message(log_id, type, message, msisdn, action):
    log = Log.query.filter_by(id=log_id).first()

    message_options = {
            'app_id': APP_ID,
            'app_secret': APP_SECRET,
            'message': message,
            'address': msisdn,
            'passphrase': PASSPHRASE,
        }

    try:
        r = requests.post(IPP_URL,message_options)           
        if r.status_code == 201:
            if action == 'entered':
                log.time_in_notification_status='Success'
            else:
                log.time_out_notification_status='Success'
            db.session.commit()
            return

        if r.json()['error'] == 'Invalid address.':
            if action == 'entered':
                log.time_in_notification_status='Invalid address'
            else:
                log.time_out_notification_status='Invalid address'
            db.session.commit()
            return

        if action == 'entered':
            log.time_in_notification_status='Failed'
        else:
            log.time_out_notification_status='Failed'
        db.session.commit()
        return

    except requests.exceptions.ConnectionError as e:
        if action == 'entered':
            log.time_in_notification_status='Failed'
        else:
            log.time_out_notification_status='Failed'
        db.session.commit()
        return

@app.task
def create_pdf(pdf_data,file_name,report_id):
    report = Report.query.filter_by(id=report_id).first()
    try:
        resultFile = open('static/reports/%s.pdf'%file_name, "w+b")
        pdf = StringIO()
        pisa.CreatePDF(StringIO(pdf_data.encode('utf-8')), dest='static/reports/%s.pdf'%file_name) 
        resultFile.close()

        report.status = 'success'
        db.session.commit()
        return

    except requests.exceptions.ConnectionError as e:
        report.status = 'failed'
        db.session.commit()
        return

def get_hour(time):
    if time[6:8] == 'PM' and time[:2] != '12':
        hour = int(time[:2]) + 12
        return hour
    elif time[6:8] == 'AM' and time[:2] == '12':
        hour = 00
        return hour
    hour = int(time[:2])
    return hour

@app.task
def check_if_late(school_no,api_key,id_no,name,level,section,date,group,log_time,timestamp):
    now = datetime.datetime.now()
    time_now = str(now.replace(hour=get_hour(log_time), minute=int(log_time[3:5])))[11:16]

    irregular_class = Irregular.query.filter_by(school_no=school_no,date=time.strftime("%B %d, %Y")).first()
    if irregular_class:
        schedule = irregular_class
    else:
        schedule = Regular.query.filter_by(school_no=school_no,day=time.strftime('%A')).first()

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

    if parse_date(time_now) >= parse_date(morning_start) and\
        parse_date(time_now) < parse_date(morning_end) and\
        Absent.query.filter_by(school_no=school_no,id_no=id_no,date=date,time_of_day='morning').first() == None:
        if morning_class:
            if parse_date(time_now) - parse_date(morning_start) > datetime.timedelta(hours=0,minutes=15):
                mark_specific_absent(school_no,id_no,'morning')
            else:
                record_as_late(school_no, id_no, name, level, section, 
                            date, group, log_time, timestamp, 'morning')

    elif (parse_date(time_now) >= parse_date(afternoon_start) and\
        parse_date(time_now) < parse_date(afternoon_end)) and\
        Absent.query.filter_by(school_no=school_no,id_no=id_no,date=date,time_of_day='afternoon').first() == None:
        if afternoon_class:
            if parse_date(time_now) - parse_date(afternoon_start) > datetime.timedelta(hours=0,minutes=15):
                mark_specific_absent(school_no,id_no,'afternoon')
            else:
                record_as_late(school_no, id_no, name, level, section, 
                            date, group, log_time, timestamp, 'afternoon')

    return

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
            department=student.group,
            section=student.section,
            time_of_day=time_of_day,
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            )
    db.session.add(absent)
    db.session.commit()

    student.absences=Absent.query.filter_by(id_no=id_no, school_no=school_no).count()
    db.session.commit()

@app.task
def afternoon_absent(school_no,api_key,level):
    all_students = K12.query.filter_by(school_no=school_no,level=level).all()

    for student in all_students:
        logged = Log.query.filter_by(date=time.strftime("%B %d, %Y"),id_no=student.id_no).order_by(Log.timestamp.desc()).first()
        marked = Absent.query.filter_by(date=time.strftime("%B %d, %Y"),id_no=student.id_no,time_of_day='afternoon').order_by(Absent.timestamp.desc()).first()
        if not logged or logged == None or logged.time_out != None:
            if not marked or marked == None:
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
                    department=student.group,
                    time_of_day='afternoon',
                    timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                    )

                db.session.add(absent)
                db.session.commit()
                if logged and logged != None and logged.time_out != None:
                    message = '%s left the campus on %s at exactly %s and did not come back.' % (student_name, logged.date, logged.time_out)
                    send_absent_message(absent.id,message,student.parent_contact)
                else:
                    absent.notification_status = 'Exempted'
                    db.session.commit()

                student.absences=Absent.query.filter_by(id_no=student.id_no, school_no=school_no).count()
                db.session.commit()
    return


@app.task
def morning_absent(school_no,api_key,level):
    students = K12.query.filter_by(school_no=school_no,level=level).all()

    for student in students:
        logged = Log.query.filter_by(date=time.strftime("%B %d, %Y"),id_no=student.id_no).order_by(Log.timestamp.desc()).first()
        marked = Absent.query.filter_by(date=time.strftime("%B %d, %Y"),id_no=student.id_no,time_of_day='morning').order_by(Absent.timestamp.desc()).first()
        if not logged or logged == None or logged.time_out != None:
            if not marked or marked == None:
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
                department=student.group,
                time_of_day='morning',
                timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                )

                db.session.add(absent)

                student.absences=Absent.query.filter_by(id_no=student.id_no, school_no=school_no).count()
                db.session.commit()
    return