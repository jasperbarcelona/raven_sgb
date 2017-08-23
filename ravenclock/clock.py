#/usr/bin/python

import flask, flask.views
from flask import url_for, request, session, redirect, jsonify, Response, make_response, current_app
from flask import render_template, request
from flask import session, redirect
from jinja2 import environment, FileSystemLoader
from flask.ext import admin
from flask.ext.admin.contrib import sqla
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin import Admin, BaseView, expose
from dateutil.parser import parse as parse_date
from functools import update_wrapper
from datetime import timedelta
from datetime import datetime
from functools import wraps
import threading
from werkzeug.datastructures import FileStorage
from werkzeug import secure_filename
import helpers.helper as helper
from time import sleep
import requests
import datetime
import time
import json
import uuid
import os

app = flask.Flask(__name__)
app.secret_key = '234234rfascasascqweqscasefsdvqwefe2323234dvsv'

class IngAdmin(sqla.ModelView):
    column_display_pk = True\
    
admin = Admin(app)
admin.add_view(IngAdmin(helper.Regular, helper.db.session))
admin.add_view(IngAdmin(helper.Irregular, helper.db.session))
admin.add_view(IngAdmin(helper.School, helper.db.session))


# @app.route('/schedule/sync',methods=['GET','POST'])
# def initialize_timer():
#     helper.sync_schedule()
#     return jsonify(status='success'),200


@app.route('/schedule/regular/update',methods=['GET','POST'])
def update_regular_sched():
    api_key = flask.request.form.get('api_key')
    schedule = flask.request.form.getlist('schedule')
    return helper.change_regular_sched(api_key,schedule)


@app.route('/schedule/irregular/new',methods=['GET','POST'])
def new_irregular_sched():
    data = flask.request.args.to_dict()
    schedule = flask.request.form.to_dict()
    return helper.save_irregular_schedule(data['api_key'],data['month'],data['day'],data['year'],schedule)


@app.route('/schedule/irregular/get',methods=['GET','POST'])
def irregular_sched():
    api_key = flask.request.args.get('api_key')
    month = flask.request.args.get('month')
    day = flask.request.args.get('day')
    year = flask.request.args.get('year')
    return helper.get_irregular_schedule(api_key,month,day,year)


@app.route('/schedule/regular/get',methods=['GET','POST'])
def regular_sched():
    api_key = flask.request.args.get('api_key')
    return helper.get_regular_schedule(api_key)


@app.route('/events/get',methods=['GET','POST'])
def get_events():
    api_key = flask.request.args.get('api_key')
    month = flask.request.args.get('month')
    year = flask.request.args.get('year')
    return helper.get_events(api_key,month,year)


@app.route('/db/rebuild',methods=['GET','POST'])
def database_rebuild():
    return helper.rebuild_database()


if __name__ == '__main__':
    helper.sync_schedule()
    app.debug = True
    app.run(port=5000, host='0.0.0.0', threaded=True, use_reloader=False)

    #port=int(os.environ['PORT']), host='0.0.0.0',