from dateutil.parser import parse as parse_date
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from flask import render_template, request, jsonify, url_for
from functools import update_wrapper
from flask import session, redirect
from datetime import timedelta
from datetime import datetime
from functools import wraps
import threading
from threading import Timer
from multiprocessing.pool import ThreadPool
import cStringIO
from werkzeug.datastructures import FileStorage
from multiprocessing.pool import ThreadPool
from werkzeug import secure_filename
from models import *
from time import sleep
import requests
import datetime
import time
import json
import uuid
import os
import db_conn as db
import json
import calendar

db = db.alchemy
now = datetime.datetime.now()

SYNC_URL = 'http://main/schedule/sync'

def get_schedule(sched_type,school_no):
    school = School.query.filter_by(school_no=school_no).first()
    if sched_type == 'regular':
        sched = Regular.query.filter_by(school_no=school_no ,day=time.strftime('%A')).first()
    else:
        sched = Irregular.query.filter_by(school_no=school_no, date=time.strftime("%B %d, %Y")).first()
    data = {
            'school_no':school_no,
            'api_key':school.api_key,
            'junior_kinder_morning_class': sched.junior_kinder_morning_class,
            'junior_kinder_afternoon_class': sched.junior_kinder_afternoon_class,
            'senior_kinder_morning_class': sched.senior_kinder_morning_class,
            'senior_kinder_afternoon_class': sched.senior_kinder_afternoon_class,
            'first_grade_morning_class': sched.first_grade_morning_class,
            'first_grade_afternoon_class': sched.first_grade_afternoon_class,
            'second_grade_morning_class': sched.second_grade_morning_class,
            'second_grade_afternoon_class': sched.second_grade_afternoon_class,
            'third_grade_morning_class': sched.third_grade_morning_class,
            'third_grade_afternoon_class': sched.third_grade_afternoon_class,
            'fourth_grade_morning_class': sched.fourth_grade_morning_class,
            'fourth_grade_afternoon_class': sched.fourth_grade_afternoon_class,
            'fifth_grade_morning_class': sched.fifth_grade_morning_class,
            'fifth_grade_afternoon_class': sched.fifth_grade_afternoon_class,
            'sixth_grade_morning_class': sched.sixth_grade_morning_class,
            'sixth_grade_afternoon_class': sched.sixth_grade_afternoon_class,
            'seventh_grade_morning_class': sched.seventh_grade_morning_class,
            'seventh_grade_afternoon_class': sched.seventh_grade_afternoon_class,
            'eight_grade_morning_class': sched.eight_grade_morning_class,
            'eight_grade_afternoon_class': sched.eight_grade_afternoon_class,
            'ninth_grade_morning_class': sched.ninth_grade_morning_class,
            'ninth_grade_afternoon_class': sched.ninth_grade_afternoon_class,
            'tenth_grade_morning_class': sched.tenth_grade_morning_class,
            'tenth_grade_afternoon_class': sched.tenth_grade_afternoon_class,
            'eleventh_grade_morning_class': sched.eleventh_grade_morning_class,
            'eleventh_grade_afternoon_class': sched.eleventh_grade_afternoon_class,
            'twelfth_grade_morning_class': sched.twelfth_grade_morning_class,
            'twelfth_grade_afternoon_class': sched.twelfth_grade_afternoon_class,

            'junior_kinder_morning_start': sched.junior_kinder_morning_start,
            'junior_kinder_morning_end': sched.junior_kinder_morning_end,
            'junior_kinder_afternoon_start': sched.junior_kinder_afternoon_start,
            'junior_kinder_afternoon_end': sched.junior_kinder_afternoon_end,
            'senior_kinder_morning_start': sched.senior_kinder_morning_start,
            'senior_kinder_morning_end': sched.senior_kinder_morning_end,
            'senior_kinder_afternoon_start': sched.senior_kinder_afternoon_start,
            'senior_kinder_afternoon_end': sched.senior_kinder_afternoon_end,
            'first_grade_morning_start': sched.first_grade_morning_start,
            'first_grade_morning_end': sched.first_grade_morning_end,
            'first_grade_afternoon_start': sched.first_grade_afternoon_start,
            'first_grade_afternoon_end': sched.first_grade_afternoon_end,
            'second_grade_morning_start': sched.second_grade_morning_start,
            'second_grade_morning_end': sched.second_grade_morning_end,
            'second_grade_afternoon_start': sched.second_grade_afternoon_start,
            'second_grade_afternoon_end': sched.second_grade_afternoon_end,
            'third_grade_morning_start': sched.third_grade_morning_start,
            'third_grade_morning_end': sched.third_grade_morning_end,
            'third_grade_afternoon_start': sched.third_grade_afternoon_start,
            'third_grade_afternoon_end': sched.third_grade_afternoon_end,
            'fourth_grade_morning_start': sched.fourth_grade_morning_start,
            'fourth_grade_morning_end': sched.fourth_grade_morning_end,
            'fourth_grade_afternoon_start': sched.fourth_grade_afternoon_start,
            'fourth_grade_afternoon_end': sched.fourth_grade_afternoon_end,
            'fifth_grade_morning_start': sched.fifth_grade_morning_start,
            'fifth_grade_morning_end': sched.fifth_grade_morning_end,
            'fifth_grade_afternoon_start': sched.fifth_grade_afternoon_start,
            'fifth_grade_afternoon_end': sched.fifth_grade_afternoon_end,
            'sixth_grade_morning_start': sched.sixth_grade_morning_start,
            'sixth_grade_morning_end': sched.sixth_grade_morning_end,
            'sixth_grade_afternoon_start': sched.sixth_grade_afternoon_start,
            'sixth_grade_afternoon_end': sched.sixth_grade_afternoon_end,
            'seventh_grade_morning_start': sched.seventh_grade_morning_start,
            'seventh_grade_morning_end': sched.seventh_grade_morning_end,
            'seventh_grade_afternoon_start': sched.seventh_grade_afternoon_start,
            'seventh_grade_afternoon_end': sched.seventh_grade_afternoon_end,
            'eight_grade_morning_start': sched.eight_grade_morning_start,
            'eight_grade_morning_end': sched.eight_grade_morning_end,
            'eight_grade_afternoon_start': sched.eight_grade_afternoon_start,
            'eight_grade_afternoon_end': sched.eight_grade_afternoon_end,
            'ninth_grade_morning_start': sched.ninth_grade_morning_start,
            'ninth_grade_morning_end': sched.ninth_grade_morning_end,
            'ninth_grade_afternoon_start': sched.ninth_grade_afternoon_start,
            'ninth_grade_afternoon_end': sched.ninth_grade_afternoon_end,
            'tenth_grade_morning_start': sched.tenth_grade_morning_start,
            'tenth_grade_morning_end': sched.tenth_grade_morning_end,
            'tenth_grade_afternoon_start': sched.tenth_grade_afternoon_start,
            'tenth_grade_afternoon_end': sched.tenth_grade_afternoon_end,
            'eleventh_grade_morning_start': sched.eleventh_grade_morning_start,
            'eleventh_grade_morning_end': sched.eleventh_grade_morning_end,
            'eleventh_grade_afternoon_start': sched.eleventh_grade_afternoon_start,
            'eleventh_grade_afternoon_end': sched.eleventh_grade_afternoon_end,
            'twelfth_grade_morning_start': sched.twelfth_grade_morning_start,
            'twelfth_grade_morning_end': sched.twelfth_grade_morning_end,
            'twelfth_grade_afternoon_start': sched.twelfth_grade_afternoon_start,
            'twelfth_grade_afternoon_end': sched.twelfth_grade_afternoon_end
        }
    return data


def get_events(api_key,month,year):
    event_days=[]
    school = School.query.filter_by(api_key=api_key).first()
    events = Irregular.query.filter_by(school_no=school.school_no,month=month,year=year).all()
    for event in events:
        event_days.append(event.day)
    return jsonify(days=event_days)


def sync_schedule():
    print 'working'
    schools = School.query.all()
    for school in schools:
        irregular_class = Irregular.query.filter_by(school_no=school.school_no,date=time.strftime("%B %d, %Y")).first()

        try:
            if irregular_class:
                r = requests.post(
                    SYNC_URL,
                    get_schedule('irregular',school.school_no)           
                )
                print 'synced irregular'
            else:
                r = requests.post(
                    SYNC_URL,
                    get_schedule('regular',school.school_no)           
                )
                print 'synced regular'

        except requests.exceptions.ConnectionError as e:
            print 'Failed'
    return

def save_irregular_schedule(api_key,month,day,year,schedule):
    school = School.query.filter_by(api_key=api_key).first()
    existing = Irregular.query.filter_by(school_no=school.school_no,month=month,day=day,year=year).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()

    irregular_schedule = Irregular(
        school_no=school.school_no,
        date=calendar.month_name[int(month)]+' '+str(day)+', '+str(year),
        day=day,
        month=month,
        year=year,
        junior_kinder_morning_class=True if schedule['save_junior_kinder_morning_class'] == 'true' else False,
        junior_kinder_afternoon_class=True if schedule['save_junior_kinder_afternoon_class'] == 'true' else False,
        senior_kinder_morning_class=True if schedule['save_senior_kinder_morning_class'] == 'true' else False,
        senior_kinder_afternoon_class=True if schedule['save_senior_kinder_afternoon_class'] == 'true' else False,
        first_grade_morning_class=True if schedule['save_first_grade_morning_class'] == 'true' else False,
        first_grade_afternoon_class=True if schedule['save_first_grade_afternoon_class'] == 'true' else False,
        second_grade_morning_class=True if schedule['save_second_grade_morning_class'] == 'true' else False,
        second_grade_afternoon_class=True if schedule['save_second_grade_afternoon_class'] == 'true' else False,
        third_grade_morning_class=True if schedule['save_third_grade_morning_class'] == 'true' else False,
        third_grade_afternoon_class=True if schedule['save_third_grade_afternoon_class'] == 'true' else False,
        fourth_grade_morning_class=True if schedule['save_fourth_grade_morning_class'] == 'true' else False,
        fourth_grade_afternoon_class=True if schedule['save_fourth_grade_afternoon_class'] == 'true' else False,
        fifth_grade_morning_class=True if schedule['save_fifth_grade_morning_class'] == 'true' else False,
        fifth_grade_afternoon_class=True if schedule['save_fifth_grade_afternoon_class'] == 'true' else False,
        sixth_grade_morning_class=True if schedule['save_sixth_grade_morning_class'] == 'true' else False,
        sixth_grade_afternoon_class=True if schedule['save_sixth_grade_afternoon_class'] == 'true' else False,
        seventh_grade_morning_class=True if schedule['save_seventh_grade_morning_class'] == 'true' else False,
        seventh_grade_afternoon_class=True if schedule['save_seventh_grade_afternoon_class'] == 'true' else False,
        eight_grade_morning_class=True if schedule['save_eight_grade_morning_class'] == 'true' else False,
        eight_grade_afternoon_class=True if schedule['save_eight_grade_afternoon_class'] == 'true' else False,
        ninth_grade_morning_class=True if schedule['save_ninth_grade_morning_class'] == 'true' else False,
        ninth_grade_afternoon_class=True if schedule['save_ninth_grade_afternoon_class'] == 'true' else False,
        tenth_grade_morning_class=True if schedule['save_tenth_grade_morning_class'] == 'true' else False,
        tenth_grade_afternoon_class=True if schedule['save_tenth_grade_afternoon_class'] == 'true' else False,
        eleventh_grade_morning_class=True if schedule['save_eleventh_grade_morning_class'] == 'true' else False,
        eleventh_grade_afternoon_class=True if schedule['save_eleventh_grade_afternoon_class'] == 'true' else False,
        twelfth_grade_morning_class=True if schedule['save_twelfth_grade_morning_class'] == 'true' else False,
        twelfth_grade_afternoon_class=True if schedule['save_twelfth_grade_afternoon_class'] == 'true' else False,

        junior_kinder_morning_start=schedule['save_junior_kinder_morning_start'],
        junior_kinder_morning_end=schedule['save_junior_kinder_morning_end'],
        junior_kinder_afternoon_start=schedule['save_junior_kinder_afternoon_start'],
        junior_kinder_afternoon_end=schedule['save_junior_kinder_afternoon_end'],
        senior_kinder_morning_start=schedule['save_senior_kinder_morning_start'],
        senior_kinder_morning_end=schedule['save_senior_kinder_morning_end'],
        senior_kinder_afternoon_start=schedule['save_senior_kinder_afternoon_start'],
        senior_kinder_afternoon_end=schedule['save_senior_kinder_afternoon_end'],
        first_grade_morning_start=schedule['save_first_grade_morning_start'],
        first_grade_morning_end=schedule['save_first_grade_morning_end'],
        first_grade_afternoon_start=schedule['save_first_grade_afternoon_start'],
        first_grade_afternoon_end=schedule['save_first_grade_afternoon_end'],
        second_grade_morning_start=schedule['save_second_grade_morning_start'],
        second_grade_morning_end=schedule['save_second_grade_morning_end'],
        second_grade_afternoon_start=schedule['save_second_grade_afternoon_start'],
        second_grade_afternoon_end=schedule['save_second_grade_afternoon_end'],
        third_grade_morning_start=schedule['save_third_grade_morning_start'],
        third_grade_morning_end=schedule['save_third_grade_morning_end'],
        third_grade_afternoon_start=schedule['save_third_grade_afternoon_start'],
        third_grade_afternoon_end=schedule['save_third_grade_afternoon_end'],
        fourth_grade_morning_start=schedule['save_fourth_grade_morning_start'],
        fourth_grade_morning_end=schedule['save_fourth_grade_morning_end'],
        fourth_grade_afternoon_start=schedule['save_fourth_grade_afternoon_start'],
        fourth_grade_afternoon_end=schedule['save_fourth_grade_afternoon_end'],
        fifth_grade_morning_start=schedule['save_fifth_grade_morning_start'],
        fifth_grade_morning_end=schedule['save_fifth_grade_morning_end'],
        fifth_grade_afternoon_start=schedule['save_fifth_grade_afternoon_start'],
        fifth_grade_afternoon_end=schedule['save_fifth_grade_afternoon_end'],
        sixth_grade_morning_start=schedule['save_sixth_grade_morning_start'],
        sixth_grade_morning_end=schedule['save_sixth_grade_morning_end'],
        sixth_grade_afternoon_start=schedule['save_sixth_grade_afternoon_start'],
        sixth_grade_afternoon_end=schedule['save_sixth_grade_afternoon_end'],
        seventh_grade_morning_start=schedule['save_seventh_grade_morning_start'],
        seventh_grade_morning_end=schedule['save_seventh_grade_morning_end'],
        seventh_grade_afternoon_start=schedule['save_seventh_grade_afternoon_start'],
        seventh_grade_afternoon_end=schedule['save_seventh_grade_afternoon_end'],
        eight_grade_morning_start=schedule['save_eight_grade_morning_start'],
        eight_grade_morning_end=schedule['save_eight_grade_morning_end'],
        eight_grade_afternoon_start=schedule['save_eight_grade_afternoon_start'],
        eight_grade_afternoon_end=schedule['save_eight_grade_afternoon_end'],
        ninth_grade_morning_start=schedule['save_ninth_grade_morning_start'],
        ninth_grade_morning_end=schedule['save_ninth_grade_morning_end'],
        ninth_grade_afternoon_start=schedule['save_ninth_grade_afternoon_start'],
        ninth_grade_afternoon_end=schedule['save_ninth_grade_afternoon_end'],
        tenth_grade_morning_start=schedule['save_tenth_grade_morning_start'],
        tenth_grade_morning_end=schedule['save_tenth_grade_morning_end'],
        tenth_grade_afternoon_start=schedule['save_tenth_grade_afternoon_start'],
        tenth_grade_afternoon_end=schedule['save_tenth_grade_afternoon_end'],
        eleventh_grade_morning_start=schedule['save_eleventh_grade_morning_start'],
        eleventh_grade_morning_end=schedule['save_eleventh_grade_morning_end'],
        eleventh_grade_afternoon_start=schedule['save_eleventh_grade_afternoon_start'],
        eleventh_grade_afternoon_end=schedule['save_eleventh_grade_afternoon_end'],
        twelfth_grade_morning_start=schedule['save_twelfth_grade_morning_start'],
        twelfth_grade_morning_end=schedule['save_twelfth_grade_morning_end'],
        twelfth_grade_afternoon_start=schedule['save_twelfth_grade_afternoon_start'],
        twelfth_grade_afternoon_end=schedule['save_twelfth_grade_afternoon_end']
        )
    db.session.add(irregular_schedule)
    db.session.commit()

    return jsonify(status='success'),201


def get_irregular_schedule(api_key,month,day,year):
    school = School.query.filter_by(api_key=api_key).first()
    schedule = Irregular.query.filter_by(school_no=school.school_no,month=month,day=day,year=year).first()
    return jsonify(
        junior_kinder_morning_class=schedule.junior_kinder_morning_class,
        junior_kinder_afternoon_class=schedule.junior_kinder_afternoon_class,
        senior_kinder_morning_class=schedule.senior_kinder_morning_class,
        senior_kinder_afternoon_class=schedule.senior_kinder_afternoon_class,
        first_grade_morning_class=schedule.first_grade_morning_class,
        first_grade_afternoon_class=schedule.first_grade_afternoon_class,
        second_grade_morning_class=schedule.second_grade_morning_class,
        second_grade_afternoon_class=schedule.second_grade_afternoon_class,
        third_grade_morning_class=schedule.third_grade_morning_class,
        third_grade_afternoon_class=schedule.third_grade_afternoon_class,
        fourth_grade_morning_class=schedule.fourth_grade_morning_class,
        fourth_grade_afternoon_class=schedule.fourth_grade_afternoon_class,
        fifth_grade_morning_class=schedule.fifth_grade_morning_class,
        fifth_grade_afternoon_class=schedule.fifth_grade_afternoon_class,
        sixth_grade_morning_class=schedule.sixth_grade_morning_class,
        sixth_grade_afternoon_class=schedule.sixth_grade_afternoon_class,
        seventh_grade_morning_class=schedule.seventh_grade_morning_class,
        seventh_grade_afternoon_class=schedule.seventh_grade_afternoon_class,
        eight_grade_morning_class=schedule.eight_grade_morning_class,
        eight_grade_afternoon_class=schedule.eight_grade_afternoon_class,
        ninth_grade_morning_class=schedule.ninth_grade_morning_class,
        ninth_grade_afternoon_class=schedule.ninth_grade_afternoon_class,
        tenth_grade_morning_class=schedule.tenth_grade_morning_class,
        tenth_grade_afternoon_class=schedule.tenth_grade_afternoon_class,
        eleventh_grade_morning_class=schedule.eleventh_grade_morning_class,
        eleventh_grade_afternoon_class=schedule.eleventh_grade_afternoon_class,
        twelfth_grade_morning_class=schedule.twelfth_grade_morning_class,
        twelfth_grade_afternoon_class=schedule.twelfth_grade_afternoon_class,
        junior_kinder_morning_start=schedule.junior_kinder_morning_start,
        junior_kinder_morning_end=schedule.junior_kinder_morning_end,
        junior_kinder_afternoon_start=schedule.junior_kinder_afternoon_start,
        junior_kinder_afternoon_end=schedule.junior_kinder_afternoon_end,
        senior_kinder_morning_start=schedule.senior_kinder_morning_start,
        senior_kinder_morning_end=schedule.senior_kinder_morning_end,
        senior_kinder_afternoon_start=schedule.senior_kinder_afternoon_start,
        senior_kinder_afternoon_end=schedule.senior_kinder_afternoon_end,
        first_grade_morning_start=schedule.first_grade_morning_start,
        first_grade_morning_end=schedule.first_grade_morning_end,
        first_grade_afternoon_start=schedule.first_grade_afternoon_start,
        first_grade_afternoon_end=schedule.first_grade_afternoon_end,
        second_grade_morning_start=schedule.second_grade_morning_start,
        second_grade_morning_end=schedule.second_grade_morning_end,
        second_grade_afternoon_start=schedule.second_grade_afternoon_start,
        second_grade_afternoon_end=schedule.second_grade_afternoon_end,
        third_grade_morning_start=schedule.third_grade_morning_start,
        third_grade_morning_end=schedule.third_grade_morning_end,
        third_grade_afternoon_start=schedule.third_grade_afternoon_start,
        third_grade_afternoon_end=schedule.third_grade_afternoon_end,
        fourth_grade_morning_start=schedule.fourth_grade_morning_start,
        fourth_grade_morning_end=schedule.fourth_grade_morning_end,
        fourth_grade_afternoon_start=schedule.fourth_grade_afternoon_start,
        fourth_grade_afternoon_end=schedule.fourth_grade_afternoon_end,
        fifth_grade_morning_start=schedule.fifth_grade_morning_start,
        fifth_grade_morning_end=schedule.fifth_grade_morning_end,
        fifth_grade_afternoon_start=schedule.fifth_grade_afternoon_start,
        fifth_grade_afternoon_end=schedule.fifth_grade_afternoon_end,
        sixth_grade_morning_start=schedule.sixth_grade_morning_start,
        sixth_grade_morning_end=schedule.sixth_grade_morning_end,
        sixth_grade_afternoon_start=schedule.sixth_grade_afternoon_start,
        sixth_grade_afternoon_end=schedule.sixth_grade_afternoon_end,
        seventh_grade_morning_start=schedule.seventh_grade_morning_start,
        seventh_grade_morning_end=schedule.seventh_grade_morning_end,
        seventh_grade_afternoon_start=schedule.seventh_grade_afternoon_start,
        seventh_grade_afternoon_end=schedule.seventh_grade_afternoon_end,
        eight_grade_morning_start=schedule.eight_grade_morning_start,
        eight_grade_morning_end=schedule.eight_grade_morning_end,
        eight_grade_afternoon_start=schedule.eight_grade_afternoon_start,
        eight_grade_afternoon_end=schedule.eight_grade_afternoon_end,
        ninth_grade_morning_start=schedule.ninth_grade_morning_start,
        ninth_grade_morning_end=schedule.ninth_grade_morning_end,
        ninth_grade_afternoon_start=schedule.ninth_grade_afternoon_start,
        ninth_grade_afternoon_end=schedule.ninth_grade_afternoon_end,
        tenth_grade_morning_start=schedule.tenth_grade_morning_start,
        tenth_grade_morning_end=schedule.tenth_grade_morning_end,
        tenth_grade_afternoon_start=schedule.tenth_grade_afternoon_start,
        tenth_grade_afternoon_end=schedule.tenth_grade_afternoon_end,
        eleventh_grade_morning_start=schedule.eleventh_grade_morning_start,
        eleventh_grade_morning_end=schedule.eleventh_grade_morning_end,
        eleventh_grade_afternoon_start=schedule.eleventh_grade_afternoon_start,
        eleventh_grade_afternoon_end=schedule.eleventh_grade_afternoon_end,
        twelfth_grade_morning_start=schedule.twelfth_grade_morning_start,
        twelfth_grade_morning_end=schedule.twelfth_grade_morning_end,
        twelfth_grade_afternoon_start=schedule.twelfth_grade_afternoon_start,
        twelfth_grade_afternoon_end=schedule.twelfth_grade_afternoon_end
        ),201


def get_regular_schedule(api_key):
    school = School.query.filter_by(api_key=api_key).first()
    monday_schedule = Regular.query.filter_by(school_no=school.school_no,day='Monday').first()
    tuesday_schedule = Regular.query.filter_by(school_no=school.school_no,day='Tuesday').first()
    wednesday_schedule = Regular.query.filter_by(school_no=school.school_no,day='Wednesday').first()
    thursday_schedule = Regular.query.filter_by(school_no=school.school_no,day='Thursday').first()
    friday_schedule = Regular.query.filter_by(school_no=school.school_no,day='Friday').first()
    return SWJsonify({
        'monday': monday_schedule,
        'tuesday': tuesday_schedule,
        'wednesday': wednesday_schedule,
        'thursday': thursday_schedule,
        'friday': friday_schedule,
        }), 200


# def start_sync_timer():
#     x = datetime.datetime.now()
#     y = x.replace(hour=14, minute=24, second=0, microsecond=0)
#     delta_t = y - x
#     secs = delta_t.seconds + 1
#     t = Timer(secs, sync_schedule)
#     t.start()
#     print 'time until sync: ' + str(secs/60) + ' min/s'


def change_regular_sched(api_key,schedule):
    school = School.query.filter_by(api_key=api_key).one()
    monday_sched = Regular.query.filter_by(school_no=school.school_no,day='Monday').one()
    tuesday_sched = Regular.query.filter_by(school_no=school.school_no,day=u'Tuesday').one()
    wednesday_sched = Regular.query.filter_by(school_no=school.school_no,day='Wednesday').one()
    thursday_sched = Regular.query.filter_by(school_no=school.school_no,day='Thursday').one()
    friday_sched = Regular.query.filter_by(school_no=school.school_no,day='Friday').one()

    monday_sched.junior_kinder_morning_start = schedule[0]
    monday_sched.junior_kinder_morning_end = schedule[1]
    monday_sched.junior_kinder_afternoon_start = schedule[2]
    monday_sched.junior_kinder_afternoon_end = schedule[3]
    monday_sched.senior_kinder_morning_start = schedule[4]
    monday_sched.senior_kinder_morning_end = schedule[5]
    monday_sched.senior_kinder_afternoon_start = schedule[6]
    monday_sched.senior_kinder_afternoon_end = schedule[7]
    monday_sched.first_grade_morning_start = schedule[8]
    monday_sched.first_grade_morning_end = schedule[9]
    monday_sched.first_grade_afternoon_start = schedule[10]
    monday_sched.first_grade_afternoon_end = schedule[11]
    monday_sched.second_grade_morning_start = schedule[12]
    monday_sched.second_grade_morning_end = schedule[13]
    monday_sched.second_grade_afternoon_start = schedule[14]
    monday_sched.second_grade_afternoon_end = schedule[15]
    monday_sched.third_grade_morning_start = schedule[16]
    monday_sched.third_grade_morning_end = schedule[17]
    monday_sched.third_grade_afternoon_start = schedule[18]
    monday_sched.third_grade_afternoon_end = schedule[19]
    monday_sched.fourth_grade_morning_start = schedule[20]
    monday_sched.fourth_grade_morning_end = schedule[21]
    monday_sched.fourth_grade_afternoon_start = schedule[22]
    monday_sched.fourth_grade_afternoon_end = schedule[23]
    monday_sched.fifth_grade_morning_start = schedule[24]
    monday_sched.fifth_grade_morning_end = schedule[25]
    monday_sched.fifth_grade_afternoon_start = schedule[26]
    monday_sched.fifth_grade_afternoon_end = schedule[27]
    monday_sched.sixth_grade_morning_start = schedule[28]
    monday_sched.sixth_grade_morning_end = schedule[29]
    monday_sched.sixth_grade_afternoon_start = schedule[30]
    monday_sched.sixth_grade_afternoon_end = schedule[31]
    monday_sched.seventh_grade_morning_start = schedule[32]
    monday_sched.seventh_grade_morning_end = schedule[33]
    monday_sched.seventh_grade_afternoon_start = schedule[34]
    monday_sched.seventh_grade_afternoon_end = schedule[35]
    monday_sched.eight_grade_morning_start = schedule[36]
    monday_sched.eight_grade_morning_end = schedule[37]
    monday_sched.eight_grade_afternoon_start = schedule[38]
    monday_sched.eight_grade_afternoon_end = schedule[39]
    monday_sched.ninth_grade_morning_start = schedule[40]
    monday_sched.ninth_grade_morning_end = schedule[41]
    monday_sched.ninth_grade_afternoon_start = schedule[42]
    monday_sched.ninth_grade_afternoon_end = schedule[43]
    monday_sched.tenth_grade_morning_start = schedule[44]
    monday_sched.tenth_grade_morning_end = schedule[45]
    monday_sched.tenth_grade_afternoon_start = schedule[46]
    monday_sched.tenth_grade_afternoon_end = schedule[47]
    monday_sched.eleventh_grade_morning_start = schedule[48]
    monday_sched.eleventh_grade_morning_end = schedule[49]
    monday_sched.eleventh_grade_afternoon_start = schedule[50]
    monday_sched.eleventh_grade_afternoon_end = schedule[51]
    monday_sched.twelfth_grade_morning_start = schedule[52]
    monday_sched.twelfth_grade_morning_end = schedule[53]
    monday_sched.twelfth_grade_afternoon_start = schedule[54]
    monday_sched.twelfth_grade_afternoon_end = schedule[55]


    tuesday_sched.junior_kinder_morning_start = schedule[56]
    tuesday_sched.junior_kinder_morning_end = schedule[57]
    tuesday_sched.junior_kinder_afternoon_start = schedule[58]
    tuesday_sched.junior_kinder_afternoon_end = schedule[59]
    tuesday_sched.senior_kinder_morning_start = schedule[60]
    tuesday_sched.senior_kinder_morning_end = schedule[61]
    tuesday_sched.senior_kinder_afternoon_start = schedule[62]
    tuesday_sched.senior_kinder_afternoon_end = schedule[63]
    tuesday_sched.first_grade_morning_start = schedule[64]
    tuesday_sched.first_grade_morning_end = schedule[65]
    tuesday_sched.first_grade_afternoon_start = schedule[66]
    tuesday_sched.first_grade_afternoon_end = schedule[67]
    tuesday_sched.second_grade_morning_start = schedule[68]
    tuesday_sched.second_grade_morning_end = schedule[69]
    tuesday_sched.second_grade_afternoon_start = schedule[70]
    tuesday_sched.second_grade_afternoon_end = schedule[71]
    tuesday_sched.third_grade_morning_start = schedule[72]
    tuesday_sched.third_grade_morning_end = schedule[73]
    tuesday_sched.third_grade_afternoon_start = schedule[74]
    tuesday_sched.third_grade_afternoon_end = schedule[75]
    tuesday_sched.fourth_grade_morning_start = schedule[76]
    tuesday_sched.fourth_grade_morning_end = schedule[77]
    tuesday_sched.fourth_grade_afternoon_start = schedule[78]
    tuesday_sched.fourth_grade_afternoon_end = schedule[79]
    tuesday_sched.fifth_grade_morning_start = schedule[80]
    tuesday_sched.fifth_grade_morning_end = schedule[81]
    tuesday_sched.fifth_grade_afternoon_start = schedule[82]
    tuesday_sched.fifth_grade_afternoon_end = schedule[83]
    tuesday_sched.sixth_grade_morning_start = schedule[84]
    tuesday_sched.sixth_grade_morning_end = schedule[85]
    tuesday_sched.sixth_grade_afternoon_start = schedule[86]
    tuesday_sched.sixth_grade_afternoon_end = schedule[87]
    tuesday_sched.seventh_grade_morning_start = schedule[88]
    tuesday_sched.seventh_grade_morning_end = schedule[89]
    tuesday_sched.seventh_grade_afternoon_start = schedule[90]
    tuesday_sched.seventh_grade_afternoon_end = schedule[91]
    tuesday_sched.eight_grade_morning_start = schedule[92]
    tuesday_sched.eight_grade_morning_end = schedule[93]
    tuesday_sched.eight_grade_afternoon_start = schedule[94]
    tuesday_sched.eight_grade_afternoon_end = schedule[95]
    tuesday_sched.ninth_grade_morning_start = schedule[96]
    tuesday_sched.ninth_grade_morning_end = schedule[97]
    tuesday_sched.ninth_grade_afternoon_start = schedule[98]
    tuesday_sched.ninth_grade_afternoon_end = schedule[99]
    tuesday_sched.tenth_grade_morning_start = schedule[100]
    tuesday_sched.tenth_grade_morning_end = schedule[101]
    tuesday_sched.tenth_grade_afternoon_start = schedule[102]
    tuesday_sched.tenth_grade_afternoon_end = schedule[103]
    tuesday_sched.eleventh_grade_morning_start = schedule[104]
    tuesday_sched.eleventh_grade_morning_end = schedule[105]
    tuesday_sched.eleventh_grade_afternoon_start = schedule[106]
    tuesday_sched.eleventh_grade_afternoon_end = schedule[107]
    tuesday_sched.twelfth_grade_morning_start = schedule[108]
    tuesday_sched.twelfth_grade_morning_end = schedule[109]
    tuesday_sched.twelfth_grade_afternoon_start = schedule[110]
    tuesday_sched.twelfth_grade_afternoon_end = schedule[111]


    wednesday_sched.junior_kinder_morning_start = schedule[112]
    wednesday_sched.junior_kinder_morning_end = schedule[113]
    wednesday_sched.junior_kinder_afternoon_start = schedule[114]
    wednesday_sched.junior_kinder_afternoon_end = schedule[115]
    wednesday_sched.senior_kinder_morning_start = schedule[116]
    wednesday_sched.senior_kinder_morning_end = schedule[117]
    wednesday_sched.senior_kinder_afternoon_start = schedule[118]
    wednesday_sched.senior_kinder_afternoon_end = schedule[119]
    wednesday_sched.first_grade_morning_start = schedule[120]
    wednesday_sched.first_grade_morning_end = schedule[121]
    wednesday_sched.first_grade_afternoon_start = schedule[122]
    wednesday_sched.first_grade_afternoon_end = schedule[123]
    wednesday_sched.second_grade_morning_start = schedule[124]
    wednesday_sched.second_grade_morning_end = schedule[125]
    wednesday_sched.second_grade_afternoon_start = schedule[126]
    wednesday_sched.second_grade_afternoon_end = schedule[127]
    wednesday_sched.third_grade_morning_start = schedule[128]
    wednesday_sched.third_grade_morning_end = schedule[129]
    wednesday_sched.third_grade_afternoon_start = schedule[130]
    wednesday_sched.third_grade_afternoon_end = schedule[131]
    wednesday_sched.fourth_grade_morning_start = schedule[132]
    wednesday_sched.fourth_grade_morning_end = schedule[133]
    wednesday_sched.fourth_grade_afternoon_start = schedule[134]
    wednesday_sched.fourth_grade_afternoon_end = schedule[135]
    wednesday_sched.fifth_grade_morning_start = schedule[136]
    wednesday_sched.fifth_grade_morning_end = schedule[137]
    wednesday_sched.fifth_grade_afternoon_start = schedule[138]
    wednesday_sched.fifth_grade_afternoon_end = schedule[139]
    wednesday_sched.sixth_grade_morning_start = schedule[140]
    wednesday_sched.sixth_grade_morning_end = schedule[141]
    wednesday_sched.sixth_grade_afternoon_start = schedule[142]
    wednesday_sched.sixth_grade_afternoon_end = schedule[143]
    wednesday_sched.seventh_grade_morning_start = schedule[144]
    wednesday_sched.seventh_grade_morning_end = schedule[145]
    wednesday_sched.seventh_grade_afternoon_start = schedule[146]
    wednesday_sched.seventh_grade_afternoon_end = schedule[147]
    wednesday_sched.eight_grade_morning_start = schedule[148]
    wednesday_sched.eight_grade_morning_end = schedule[149]
    wednesday_sched.eight_grade_afternoon_start = schedule[150]
    wednesday_sched.eight_grade_afternoon_end = schedule[151]
    wednesday_sched.ninth_grade_morning_start = schedule[152]
    wednesday_sched.ninth_grade_morning_end = schedule[153]
    wednesday_sched.ninth_grade_afternoon_start = schedule[154]
    wednesday_sched.ninth_grade_afternoon_end = schedule[155]
    wednesday_sched.tenth_grade_morning_start = schedule[156]
    wednesday_sched.tenth_grade_morning_end = schedule[157]
    wednesday_sched.tenth_grade_afternoon_start = schedule[158]
    wednesday_sched.tenth_grade_afternoon_end = schedule[159]
    wednesday_sched.eleventh_grade_morning_start = schedule[160]
    wednesday_sched.eleventh_grade_morning_end = schedule[161]
    wednesday_sched.eleventh_grade_afternoon_start = schedule[162]
    wednesday_sched.eleventh_grade_afternoon_end = schedule[163]
    wednesday_sched.twelfth_grade_morning_start = schedule[164]
    wednesday_sched.twelfth_grade_morning_end = schedule[165]
    wednesday_sched.twelfth_grade_afternoon_start = schedule[166]
    wednesday_sched.twelfth_grade_afternoon_end = schedule[167]


    thursday_sched.junior_kinder_morning_start = schedule[168]
    thursday_sched.junior_kinder_morning_end = schedule[169]
    thursday_sched.junior_kinder_afternoon_start = schedule[170]
    thursday_sched.junior_kinder_afternoon_end = schedule[171]
    thursday_sched.senior_kinder_morning_start = schedule[172]
    thursday_sched.senior_kinder_morning_end = schedule[173]
    thursday_sched.senior_kinder_afternoon_start = schedule[174]
    thursday_sched.senior_kinder_afternoon_end = schedule[175]
    thursday_sched.first_grade_morning_start = schedule[176]
    thursday_sched.first_grade_morning_end = schedule[177]
    thursday_sched.first_grade_afternoon_start = schedule[178]
    thursday_sched.first_grade_afternoon_end = schedule[179]
    thursday_sched.second_grade_morning_start = schedule[180]
    thursday_sched.second_grade_morning_end = schedule[181]
    thursday_sched.second_grade_afternoon_start = schedule[182]
    thursday_sched.second_grade_afternoon_end = schedule[183]
    thursday_sched.third_grade_morning_start = schedule[184]
    thursday_sched.third_grade_morning_end = schedule[185]
    thursday_sched.third_grade_afternoon_start = schedule[186]
    thursday_sched.third_grade_afternoon_end = schedule[187]
    thursday_sched.fourth_grade_morning_start = schedule[188]
    thursday_sched.fourth_grade_morning_end = schedule[189]
    thursday_sched.fourth_grade_afternoon_start = schedule[190]
    thursday_sched.fourth_grade_afternoon_end = schedule[191]
    thursday_sched.fifth_grade_morning_start = schedule[192]
    thursday_sched.fifth_grade_morning_end = schedule[193]
    thursday_sched.fifth_grade_afternoon_start = schedule[194]
    thursday_sched.fifth_grade_afternoon_end = schedule[195]
    thursday_sched.sixth_grade_morning_start = schedule[196]
    thursday_sched.sixth_grade_morning_end = schedule[197]
    thursday_sched.sixth_grade_afternoon_start = schedule[198]
    thursday_sched.sixth_grade_afternoon_end = schedule[199]
    thursday_sched.seventh_grade_morning_start = schedule[200]
    thursday_sched.seventh_grade_morning_end = schedule[201]
    thursday_sched.seventh_grade_afternoon_start = schedule[202]
    thursday_sched.seventh_grade_afternoon_end = schedule[203]
    thursday_sched.eight_grade_morning_start = schedule[204]
    thursday_sched.eight_grade_morning_end = schedule[205]
    thursday_sched.eight_grade_afternoon_start = schedule[206]
    thursday_sched.eight_grade_afternoon_end = schedule[207]
    thursday_sched.ninth_grade_morning_start = schedule[208]
    thursday_sched.ninth_grade_morning_end = schedule[209]
    thursday_sched.ninth_grade_afternoon_start = schedule[210]
    thursday_sched.ninth_grade_afternoon_end = schedule[211]
    thursday_sched.tenth_grade_morning_start = schedule[212]
    thursday_sched.tenth_grade_morning_end = schedule[213]
    thursday_sched.tenth_grade_afternoon_start = schedule[214]
    thursday_sched.tenth_grade_afternoon_end = schedule[215]
    thursday_sched.eleventh_grade_morning_start = schedule[216]
    thursday_sched.eleventh_grade_morning_end = schedule[217]
    thursday_sched.eleventh_grade_afternoon_start = schedule[218]
    thursday_sched.eleventh_grade_afternoon_end = schedule[219]
    thursday_sched.twelfth_grade_morning_start = schedule[220]
    thursday_sched.twelfth_grade_morning_end = schedule[221]
    thursday_sched.twelfth_grade_afternoon_start = schedule[222]
    thursday_sched.twelfth_grade_afternoon_end = schedule[223]


    friday_sched.junior_kinder_morning_start = schedule[224]
    friday_sched.junior_kinder_morning_end = schedule[225]
    friday_sched.junior_kinder_afternoon_start = schedule[226]
    friday_sched.junior_kinder_afternoon_end = schedule[227]
    friday_sched.senior_kinder_morning_start = schedule[228]
    friday_sched.senior_kinder_morning_end = schedule[229]
    friday_sched.senior_kinder_afternoon_start = schedule[230]
    friday_sched.senior_kinder_afternoon_end = schedule[231]
    friday_sched.first_grade_morning_start = schedule[232]
    friday_sched.first_grade_morning_end = schedule[233]
    friday_sched.first_grade_afternoon_start = schedule[234]
    friday_sched.first_grade_afternoon_end = schedule[235]
    friday_sched.second_grade_morning_start = schedule[236]
    friday_sched.second_grade_morning_end = schedule[237]
    friday_sched.second_grade_afternoon_start = schedule[238]
    friday_sched.second_grade_afternoon_end = schedule[239]
    friday_sched.third_grade_morning_start = schedule[240]
    friday_sched.third_grade_morning_end = schedule[241]
    friday_sched.third_grade_afternoon_start = schedule[242]
    friday_sched.third_grade_afternoon_end = schedule[243]
    friday_sched.fourth_grade_morning_start = schedule[244]
    friday_sched.fourth_grade_morning_end = schedule[245]
    friday_sched.fourth_grade_afternoon_start = schedule[246]
    friday_sched.fourth_grade_afternoon_end = schedule[247]
    friday_sched.fifth_grade_morning_start = schedule[248]
    friday_sched.fifth_grade_morning_end = schedule[249]
    friday_sched.fifth_grade_afternoon_start = schedule[250]
    friday_sched.fifth_grade_afternoon_end = schedule[251]
    friday_sched.sixth_grade_morning_start = schedule[252]
    friday_sched.sixth_grade_morning_end = schedule[253]
    friday_sched.sixth_grade_afternoon_start = schedule[254]
    friday_sched.sixth_grade_afternoon_end = schedule[255]
    friday_sched.seventh_grade_morning_start = schedule[256]
    friday_sched.seventh_grade_morning_end = schedule[257]
    friday_sched.seventh_grade_afternoon_start = schedule[258]
    friday_sched.seventh_grade_afternoon_end = schedule[259]
    friday_sched.eight_grade_morning_start = schedule[260]
    friday_sched.eight_grade_morning_end = schedule[261]
    friday_sched.eight_grade_afternoon_start = schedule[262]
    friday_sched.eight_grade_afternoon_end = schedule[263]
    friday_sched.ninth_grade_morning_start = schedule[264]
    friday_sched.ninth_grade_morning_end = schedule[265]
    friday_sched.ninth_grade_afternoon_start = schedule[266]
    friday_sched.ninth_grade_afternoon_end = schedule[267]
    friday_sched.tenth_grade_morning_start = schedule[268]
    friday_sched.tenth_grade_morning_end = schedule[269]
    friday_sched.tenth_grade_afternoon_start = schedule[270]
    friday_sched.tenth_grade_afternoon_end = schedule[271]
    friday_sched.eleventh_grade_morning_start = schedule[272]
    friday_sched.eleventh_grade_morning_end = schedule[273]
    friday_sched.eleventh_grade_afternoon_start = schedule[274]
    friday_sched.eleventh_grade_afternoon_end = schedule[275]
    friday_sched.twelfth_grade_morning_start = schedule[276]
    friday_sched.twelfth_grade_morning_end = schedule[277]
    friday_sched.twelfth_grade_afternoon_start = schedule[278]
    friday_sched.twelfth_grade_afternoon_end = schedule[279]

    db.session.commit()
    
    return '',201



def rebuild_database():
    db.drop_all()
    db.create_all()

    irreg2 = Irregular(
        school_no='123456789',
        date=time.strftime("%B %d, %Y"),
        day=5,
        month=1,
        year=2016,
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

    sched2 = Regular(
        school_no='123456789',
        day='Monday',
        junior_kinder_morning_class=True,
        junior_kinder_afternoon_class=True,
        senior_kinder_morning_class=True,
        senior_kinder_afternoon_class=True,
        first_grade_morning_class=True,
        first_grade_afternoon_class=True,
        second_grade_morning_class=True,
        second_grade_afternoon_class=True,
        third_grade_morning_class=True,
        third_grade_afternoon_class=True,
        fourth_grade_morning_class=True,
        fourth_grade_afternoon_class=True,
        fifth_grade_morning_class=True,
        fifth_grade_afternoon_class=True,
        sixth_grade_morning_class=True,
        sixth_grade_afternoon_class=True,
        seventh_grade_morning_class=True,
        seventh_grade_afternoon_class=True,
        eight_grade_morning_class=True,
        eight_grade_afternoon_class=True,
        ninth_grade_morning_class=True,
        ninth_grade_afternoon_class=True,
        tenth_grade_morning_class=True,
        tenth_grade_afternoon_class=True,
        eleventh_grade_morning_class=True,
        eleventh_grade_afternoon_class=True,
        twelfth_grade_morning_class=True,
        twelfth_grade_afternoon_class=True,


        junior_kinder_morning_start=str(now.replace(hour=7, minute=0, second=0))[11:16],
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

    sched3 = Regular(
        school_no='123456789',
        day='Tuesday',
        junior_kinder_morning_class=True,
        junior_kinder_afternoon_class=True,
        senior_kinder_morning_class=True,
        senior_kinder_afternoon_class=True,
        first_grade_morning_class=True,
        first_grade_afternoon_class=True,
        second_grade_morning_class=True,
        second_grade_afternoon_class=True,
        third_grade_morning_class=True,
        third_grade_afternoon_class=True,
        fourth_grade_morning_class=True,
        fourth_grade_afternoon_class=True,
        fifth_grade_morning_class=True,
        fifth_grade_afternoon_class=True,
        sixth_grade_morning_class=True,
        sixth_grade_afternoon_class=True,
        seventh_grade_morning_class=True,
        seventh_grade_afternoon_class=True,
        eight_grade_morning_class=True,
        eight_grade_afternoon_class=True,
        ninth_grade_morning_class=True,
        ninth_grade_afternoon_class=True,
        tenth_grade_morning_class=True,
        tenth_grade_afternoon_class=True,
        eleventh_grade_morning_class=True,
        eleventh_grade_afternoon_class=True,
        twelfth_grade_morning_class=True,
        twelfth_grade_afternoon_class=True,


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

    sched4 = Regular(
        school_no='123456789',
        day='Wednesday',
        junior_kinder_morning_class=True,
        junior_kinder_afternoon_class=True,
        senior_kinder_morning_class=True,
        senior_kinder_afternoon_class=True,
        first_grade_morning_class=True,
        first_grade_afternoon_class=True,
        second_grade_morning_class=True,
        second_grade_afternoon_class=True,
        third_grade_morning_class=True,
        third_grade_afternoon_class=True,
        fourth_grade_morning_class=True,
        fourth_grade_afternoon_class=True,
        fifth_grade_morning_class=True,
        fifth_grade_afternoon_class=True,
        sixth_grade_morning_class=True,
        sixth_grade_afternoon_class=True,
        seventh_grade_morning_class=True,
        seventh_grade_afternoon_class=True,
        eight_grade_morning_class=True,
        eight_grade_afternoon_class=True,
        ninth_grade_morning_class=True,
        ninth_grade_afternoon_class=True,
        tenth_grade_morning_class=True,
        tenth_grade_afternoon_class=True,
        eleventh_grade_morning_class=True,
        eleventh_grade_afternoon_class=True,
        twelfth_grade_morning_class=True,
        twelfth_grade_afternoon_class=True,


        junior_kinder_morning_start=str(now.replace(hour=9, minute=0, second=0))[11:16],
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

    sched5 = Regular(
        school_no='123456789',
        day='Thursday',
        junior_kinder_morning_class=True,
        junior_kinder_afternoon_class=True,
        senior_kinder_morning_class=True,
        senior_kinder_afternoon_class=True,
        first_grade_morning_class=True,
        first_grade_afternoon_class=True,
        second_grade_morning_class=True,
        second_grade_afternoon_class=True,
        third_grade_morning_class=True,
        third_grade_afternoon_class=True,
        fourth_grade_morning_class=True,
        fourth_grade_afternoon_class=True,
        fifth_grade_morning_class=True,
        fifth_grade_afternoon_class=True,
        sixth_grade_morning_class=True,
        sixth_grade_afternoon_class=True,
        seventh_grade_morning_class=True,
        seventh_grade_afternoon_class=True,
        eight_grade_morning_class=True,
        eight_grade_afternoon_class=True,
        ninth_grade_morning_class=True,
        ninth_grade_afternoon_class=True,
        tenth_grade_morning_class=True,
        tenth_grade_afternoon_class=True,
        eleventh_grade_morning_class=True,
        eleventh_grade_afternoon_class=True,
        twelfth_grade_morning_class=True,
        twelfth_grade_afternoon_class=True,


        junior_kinder_morning_start=str(now.replace(hour=10, minute=0, second=0))[11:16],
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

    sched6 = Regular(
        school_no='123456789',
        day='Friday',
        junior_kinder_morning_class=True,
        junior_kinder_afternoon_class=True,
        senior_kinder_morning_class=True,
        senior_kinder_afternoon_class=True,
        first_grade_morning_class=True,
        first_grade_afternoon_class=True,
        second_grade_morning_class=True,
        second_grade_afternoon_class=True,
        third_grade_morning_class=True,
        third_grade_afternoon_class=True,
        fourth_grade_morning_class=True,
        fourth_grade_afternoon_class=True,
        fifth_grade_morning_class=True,
        fifth_grade_afternoon_class=True,
        sixth_grade_morning_class=True,
        sixth_grade_afternoon_class=True,
        seventh_grade_morning_class=True,
        seventh_grade_afternoon_class=True,
        eight_grade_morning_class=True,
        eight_grade_afternoon_class=True,
        ninth_grade_morning_class=True,
        ninth_grade_afternoon_class=True,
        tenth_grade_morning_class=True,
        tenth_grade_afternoon_class=True,
        eleventh_grade_morning_class=True,
        eleventh_grade_afternoon_class=True,
        twelfth_grade_morning_class=True,
        twelfth_grade_afternoon_class=True,


        junior_kinder_morning_start=str(now.replace(hour=11, minute=0, second=0))[11:16],
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

    school2 = School(
        school_no='123456789',
        api_key='ecc67d28db284a2fb351d58fe18965f9',
        name='Sacred Heart College'
        )

    db.session.add(sched2)
    db.session.add(sched3)
    db.session.add(sched4)
    db.session.add(sched5)
    db.session.add(sched6)
    db.session.add(irreg2)
    db.session.add(school2)
    db.session.commit()

    return jsonify(status='success'), 201