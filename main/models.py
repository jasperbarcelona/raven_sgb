import flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import Boolean
from db_conn import db, app
import json
import datetime

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
    __public__= ['school_no','api_key','name','address','city','email','contact']
    id = db.Column(db.Integer,primary_key=True)
    school_no = db.Column(db.String(32), unique=True)
    api_key = db.Column(db.String(32))
    name = db.Column(db.String(50))
    address = db.Column(db.String(120))
    city = db.Column(db.String(30))
    email = db.Column(db.String(60))
    contact = db.Column(db.String(15))

class Report(db.Model, Serializer):
    id = db.Column(db.Integer,primary_key=True)
    school_no = db.Column(db.String(32))
    name = db.Column(db.String(60))
    report_type = db.Column(db.String(60))
    from_date = db.Column(db.String(30))
    to_date = db.Column(db.String(30))
    staff_name = db.Column(db.String(60))
    staff_id = db.Column(db.Integer())
    date = db.Column(db.String(50))
    time = db.Column(db.String(30))
    status = db.Column(db.String(30),default='pending')
    timestamp = db.Column(db.String(50))

class AdminUser(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    school_no = db.Column(db.String(32))
    email = db.Column(db.String(60))
    password = db.Column(db.String(20))
    name = db.Column(db.String(100))
    status = db.Column(db.String(8), default='Active')
    added_by = db.Column(db.Integer)
    students_access = db.Column(db.String(30))
    staff_access = db.Column(db.String(30))
    logs_access = db.Column(db.String(30))
    attendance_access = db.Column(db.String(30))
    wallet_access = db.Column(db.String(30))
    fees_access = db.Column(db.String(30))
    transactions_access = db.Column(db.String(30))
    accounts_access = db.Column(db.String(30))
    broadcast_access = db.Column(db.String(30))
    schedule_access = db.Column(db.String(30))
    calendar_access = db.Column(db.String(30))
    new_id_access = db.Column(db.String(30))
    join_date = db.Column(db.String(50))
    timestamp = db.Column(db.String(50))

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    junior_kinder_morning_class = db.Column(Boolean, unique=False)
    junior_kinder_afternoon_class = db.Column(Boolean, unique=False)
    senior_kinder_morning_class = db.Column(Boolean, unique=False)
    senior_kinder_afternoon_class = db.Column(Boolean, unique=False)
    first_grade_morning_class = db.Column(Boolean, unique=False)
    first_grade_afternoon_class = db.Column(Boolean, unique=False)
    second_grade_morning_class = db.Column(Boolean, unique=False)
    second_grade_afternoon_class = db.Column(Boolean, unique=False)
    third_grade_morning_class = db.Column(Boolean, unique=False)
    third_grade_afternoon_class = db.Column(Boolean, unique=False)
    fourth_grade_morning_class = db.Column(Boolean, unique=False)
    fourth_grade_afternoon_class = db.Column(Boolean, unique=False)
    fifth_grade_morning_class = db.Column(Boolean, unique=False)
    fifth_grade_afternoon_class = db.Column(Boolean, unique=False)
    sixth_grade_morning_class = db.Column(Boolean, unique=False)
    sixth_grade_afternoon_class = db.Column(Boolean, unique=False)
    seventh_grade_morning_class = db.Column(Boolean, unique=False)
    seventh_grade_afternoon_class = db.Column(Boolean, unique=False)
    eight_grade_morning_class = db.Column(Boolean, unique=False)
    eight_grade_afternoon_class = db.Column(Boolean, unique=False)
    ninth_grade_morning_class = db.Column(Boolean, unique=False)
    ninth_grade_afternoon_class = db.Column(Boolean, unique=False)
    tenth_grade_morning_class = db.Column(Boolean, unique=False)
    tenth_grade_afternoon_class = db.Column(Boolean, unique=False)
    eleventh_grade_morning_class = db.Column(Boolean, unique=False)
    eleventh_grade_afternoon_class = db.Column(Boolean, unique=False)
    twelfth_grade_morning_class = db.Column(Boolean, unique=False)
    twelfth_grade_afternoon_class = db.Column(Boolean, unique=False)

    junior_kinder_morning_start = db.Column(db.String(30))
    junior_kinder_morning_end = db.Column(db.String(30))
    junior_kinder_afternoon_start = db.Column(db.String(30))
    junior_kinder_afternoon_end = db.Column(db.String(30))
    senior_kinder_morning_start = db.Column(db.String(30))
    senior_kinder_morning_end = db.Column(db.String(30))
    senior_kinder_afternoon_start = db.Column(db.String(30))
    senior_kinder_afternoon_end = db.Column(db.String(30))
    first_grade_morning_start = db.Column(db.String(30))
    first_grade_morning_end = db.Column(db.String(30))
    first_grade_afternoon_start = db.Column(db.String(30))
    first_grade_afternoon_end = db.Column(db.String(30))
    second_grade_morning_start = db.Column(db.String(30))
    second_grade_morning_end = db.Column(db.String(30))
    second_grade_afternoon_start = db.Column(db.String(30))
    second_grade_afternoon_end = db.Column(db.String(30))

    third_grade_morning_start = db.Column(db.String(30))
    third_grade_morning_end = db.Column(db.String(30))
    third_grade_afternoon_start = db.Column(db.String(30))
    third_grade_afternoon_end = db.Column(db.String(30))

    fourth_grade_morning_start = db.Column(db.String(30))
    fourth_grade_morning_end = db.Column(db.String(30))
    fourth_grade_afternoon_start = db.Column(db.String(30))
    fourth_grade_afternoon_end = db.Column(db.String(30))

    fifth_grade_morning_start = db.Column(db.String(30))
    fifth_grade_morning_end = db.Column(db.String(30))
    fifth_grade_afternoon_start = db.Column(db.String(30))
    fifth_grade_afternoon_end = db.Column(db.String(30))

    sixth_grade_morning_start = db.Column(db.String(30))
    sixth_grade_morning_end = db.Column(db.String(30))
    sixth_grade_afternoon_start = db.Column(db.String(30))
    sixth_grade_afternoon_end = db.Column(db.String(30))

    seventh_grade_morning_start = db.Column(db.String(30))
    seventh_grade_morning_end = db.Column(db.String(30))
    seventh_grade_afternoon_start = db.Column(db.String(30))
    seventh_grade_afternoon_end = db.Column(db.String(30))

    eight_grade_morning_start = db.Column(db.String(30))
    eight_grade_morning_end = db.Column(db.String(30))
    eight_grade_afternoon_start = db.Column(db.String(30))
    eight_grade_afternoon_end = db.Column(db.String(30))

    ninth_grade_morning_start = db.Column(db.String(30))
    ninth_grade_morning_end = db.Column(db.String(30))
    ninth_grade_afternoon_start = db.Column(db.String(30))
    ninth_grade_afternoon_end = db.Column(db.String(30))

    tenth_grade_morning_start = db.Column(db.String(30))
    tenth_grade_morning_end = db.Column(db.String(30))
    tenth_grade_afternoon_start = db.Column(db.String(30))
    tenth_grade_afternoon_end = db.Column(db.String(30))

    eleventh_grade_morning_start = db.Column(db.String(30))
    eleventh_grade_morning_end = db.Column(db.String(30))
    eleventh_grade_afternoon_start = db.Column(db.String(30))
    eleventh_grade_afternoon_end = db.Column(db.String(30))

    twelfth_grade_morning_start = db.Column(db.String(30))
    twelfth_grade_morning_end = db.Column(db.String(30))
    twelfth_grade_afternoon_start = db.Column(db.String(30))
    twelfth_grade_afternoon_end = db.Column(db.String(30))

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    name = db.Column(db.String(30))

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    student_id = db.Column(db.Integer())
    student_name = db.Column(db.String(60))
    id_no = db.Column(db.String(20))
    credits = db.Column(db.Float(),default=0)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    app_key = db.Column(db.String(32))
    name = db.Column(db.String(30))
    vendor = db.Column(db.String(30),default=None)
    device_type = db.Column(db.String(30))
    added_by = db.Column(db.String(60))

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_user_id = db.Column(db.Integer)
    module_name = db.Column(db.String(60))
    privilege = db.Column(db.String(60))

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    name = db.Column(db.String(30))

class CollegeDepartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    name = db.Column(db.String(30))

class StaffDepartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    name = db.Column(db.String(30))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    sender_id = db.Column(db.Integer())
    batch_size = db.Column(db.Integer())
    done = db.Column(db.Integer(),default=0)
    pending = db.Column(db.Integer(),default=0)
    failed = db.Column(db.Integer(),default=0)
    sender_name = db.Column(db.String(60))
    recipient = db.Column(db.Text())
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    content = db.Column(db.Text)
    timestamp = db.Column(db.String(50))

class MessageStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer())
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    recipient_name = db.Column(db.String(100))
    msisdn = db.Column(db.String(30))
    status = db.Column(db.String(30),default='pending')
    timestamp = db.Column(db.String(50))

class Topup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    student_id = db.Column(db.Integer())
    student_name = db.Column(db.String(60))
    id_no = db.Column(db.String(20))
    amount = db.Column(db.Float())
    timestamp = db.Column(db.String(50))

class Log(db.Model, Serializer):
    __public__ = ['id','school_no','date','id_no','name',
                  'group','time_in','time_out','timestamp']
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    date = db.Column(db.String(20))
    id_no = db.Column(db.String(20))
    name = db.Column(db.String(60))
    group = db.Column(db.String(30))
    time_in = db.Column(db.String(10))
    time_in_id = db.Column(db.Integer)
    time_in_notification_status = db.Column(db.String(60), unique=False)
    time_out = db.Column(db.String(10),default=None)
    time_out_id = db.Column(db.Integer)
    time_out_notification_status = db.Column(db.String(60), unique=False)
    timestamp = db.Column(db.String(50))

class K12(db.Model, Serializer):
    __public__ = ['id','school_no','id_no','first_name','last_name','middle_name',
                  'level','group','section','absences','lates','parent_id','parent_relation',
                  'parent_contact','added_by']
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    id_no = db.Column(db.String(20))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    middle_name = db.Column(db.String(30))
    level = db.Column(db.String(30), default='None')
    group = db.Column(db.String(30))
    section = db.Column(db.String(30), default='None')
    absences = db.Column(db.String(3))
    lates = db.Column(db.String(3))
    parent_id = db.Column(db.Integer)
    parent_relation = db.Column(db.String(30))
    parent_contact = db.Column(db.String(30))
    image = db.Column(db.Text())
    added_by = db.Column(db.String(60))

class College(db.Model, Serializer):
    __public__ = ['id','school_no','id_no','first_name','last_name','middle_name',
                  'level','department','group','email','mobile','added_by']
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    id_no = db.Column(db.String(20))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    middle_name = db.Column(db.String(30))
    level = db.Column(db.String(30), default='None')
    department = db.Column(db.String(30))
    group = db.Column(db.String(30))
    email = db.Column(db.String(30))
    mobile = db.Column(db.String(12))
    image = db.Column(db.Text())
    added_by = db.Column(db.String(60))

class Staff(db.Model, Serializer):
    __public__ = ['id','school_no','id_no','first_name','last_name','middle_name',
                  'department','group','email','mobile','added_by']
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    id_no = db.Column(db.String(20))
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    middle_name = db.Column(db.String(30))
    department = db.Column(db.String(30))
    group = db.Column(db.String(30))
    email = db.Column(db.String(30))
    mobile = db.Column(db.String(12))
    image = db.Column(db.Text())
    added_by = db.Column(db.String(60))

class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    mobile_number = db.Column(db.String(30))
    name = db.Column(db.String(100))
    email = db.Column(db.String(60))
    address = db.Column(db.Text())

class Late(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    date = db.Column(db.String(20))
    id_no = db.Column(db.String(20))
    name = db.Column(db.String(100))
    level = db.Column(db.String(30))
    section = db.Column(db.String(30))
    time_in = db.Column(db.String(10))
    department = db.Column(db.String(30))
    time_of_day = db.Column(db.String(20))
    timestamp = db.Column(db.String(50))

class Absent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    date = db.Column(db.String(20))
    id_no = db.Column(db.String(20))
    name = db.Column(db.String(100))
    level = db.Column(db.String(30))
    section = db.Column(db.String(30))
    department = db.Column(db.String(30))
    time_of_day = db.Column(db.String(20))
    notification_status = db.Column(db.String(60), unique=False)
    timestamp = db.Column(db.String(50))

class Fee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    name = db.Column(db.String(60))
    category = db.Column(db.String(60))
    desc = db.Column(db.Text())
    price = db.Column(db.Float())
    timestamp = db.Column(db.String(50))

class StudentFee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    student_id = db.Column(db.Integer)
    fee_id = db.Column(db.Integer)
    student_name =  db.Column(db.String(100))
    fee_name = db.Column(db.String(60))
    fee_category = db.Column(db.String(60))
    fee_price = db.Column(db.Float())
    timestamp = db.Column(db.String(50))

class FeeGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    fee_id = db.Column(db.Integer)
    level = db.Column(db.String(30))

class Collected(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    student_id = db.Column(db.Integer)
    amount = db.Column(db.Float())
    date = db.Column(db.String(20))
    time = db.Column(db.String(10))
    timestamp = db.Column(db.String(50))

class FeeCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    name = db.Column(db.String(60))

class Transaction(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    date = db.Column(db.String(30))
    time = db.Column(db.String(10))
    vendor_id = db.Column(db.Integer())
    vendor_name = db.Column(db.String(30))
    cashier_id = db.Column(db.Integer())
    cashier_name = db.Column(db.String(60))
    total = db.Column(db.Float())
    amount_tendered = db.Column(db.Float(),default=0)
    change = db.Column(db.Float(),default=0)
    customer_name = db.Column(db.String(60))
    customer_id_no = db.Column(db.Integer())
    status = db.Column(db.String(60),default='Pending')
    remarks = db.Column(db.String(60),default='Pending')
    payed = db.Column(db.Boolean())
    note = db.Column(db.Text())
    timestamp = db.Column(db.String(50))
    transaction_type = db.Column(db.String(10))

class TransactionItem(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    item_name = db.Column(db.String(100))
    item_qty = db.Column(db.Integer())
    price = db.Column(db.Float())
    done = db.Column(db.Boolean())
    flavor_id = db.Column(db.Integer)

class Sale(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    date = db.Column(db.String(30))
    vendor = db.Column(db.String(30))
    cash_total = db.Column(db.Float())
    wallet_total = db.Column(db.Float())
    grand_total = db.Column(db.Float())

class Irregular(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    date = db.Column(db.String(20))
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)

    junior_kinder_morning_class = db.Column(Boolean, unique=False)
    junior_kinder_afternoon_class = db.Column(Boolean, unique=False)
    senior_kinder_morning_class = db.Column(Boolean, unique=False)
    senior_kinder_afternoon_class = db.Column(Boolean, unique=False)
    first_grade_morning_class = db.Column(Boolean, unique=False)
    first_grade_afternoon_class = db.Column(Boolean, unique=False)
    second_grade_morning_class = db.Column(Boolean, unique=False)
    second_grade_afternoon_class = db.Column(Boolean, unique=False)
    third_grade_morning_class = db.Column(Boolean, unique=False)
    third_grade_afternoon_class = db.Column(Boolean, unique=False)
    fourth_grade_morning_class = db.Column(Boolean, unique=False)
    fourth_grade_afternoon_class = db.Column(Boolean, unique=False)
    fifth_grade_morning_class = db.Column(Boolean, unique=False)
    fifth_grade_afternoon_class = db.Column(Boolean, unique=False)
    sixth_grade_morning_class = db.Column(Boolean, unique=False)
    sixth_grade_afternoon_class = db.Column(Boolean, unique=False)
    seventh_grade_morning_class = db.Column(Boolean, unique=False)
    seventh_grade_afternoon_class = db.Column(Boolean, unique=False)
    eight_grade_morning_class = db.Column(Boolean, unique=False)
    eight_grade_afternoon_class = db.Column(Boolean, unique=False)
    ninth_grade_morning_class = db.Column(Boolean, unique=False)
    ninth_grade_afternoon_class = db.Column(Boolean, unique=False)
    tenth_grade_morning_class = db.Column(Boolean, unique=False)
    tenth_grade_afternoon_class = db.Column(Boolean, unique=False)
    eleventh_grade_morning_class = db.Column(Boolean, unique=False)
    eleventh_grade_afternoon_class = db.Column(Boolean, unique=False)
    twelfth_grade_morning_class = db.Column(Boolean, unique=False)
    twelfth_grade_afternoon_class = db.Column(Boolean, unique=False)

    junior_kinder_morning_start = db.Column(db.String(30))
    junior_kinder_morning_end = db.Column(db.String(30))
    junior_kinder_afternoon_start = db.Column(db.String(30))
    junior_kinder_afternoon_end = db.Column(db.String(30))
    senior_kinder_morning_start = db.Column(db.String(30))
    senior_kinder_morning_end = db.Column(db.String(30))
    senior_kinder_afternoon_start = db.Column(db.String(30))
    senior_kinder_afternoon_end = db.Column(db.String(30))
    first_grade_morning_start = db.Column(db.String(30))
    first_grade_morning_end = db.Column(db.String(30))
    first_grade_afternoon_start = db.Column(db.String(30))
    first_grade_afternoon_end = db.Column(db.String(30))
    second_grade_morning_start = db.Column(db.String(30))
    second_grade_morning_end = db.Column(db.String(30))
    second_grade_afternoon_start = db.Column(db.String(30))
    second_grade_afternoon_end = db.Column(db.String(30))

    third_grade_morning_start = db.Column(db.String(30))
    third_grade_morning_end = db.Column(db.String(30))
    third_grade_afternoon_start = db.Column(db.String(30))
    third_grade_afternoon_end = db.Column(db.String(30))

    fourth_grade_morning_start = db.Column(db.String(30))
    fourth_grade_morning_end = db.Column(db.String(30))
    fourth_grade_afternoon_start = db.Column(db.String(30))
    fourth_grade_afternoon_end = db.Column(db.String(30))

    fifth_grade_morning_start = db.Column(db.String(30))
    fifth_grade_morning_end = db.Column(db.String(30))
    fifth_grade_afternoon_start = db.Column(db.String(30))
    fifth_grade_afternoon_end = db.Column(db.String(30))

    sixth_grade_morning_start = db.Column(db.String(30))
    sixth_grade_morning_end = db.Column(db.String(30))
    sixth_grade_afternoon_start = db.Column(db.String(30))
    sixth_grade_afternoon_end = db.Column(db.String(30))

    seventh_grade_morning_start = db.Column(db.String(30))
    seventh_grade_morning_end = db.Column(db.String(30))
    seventh_grade_afternoon_start = db.Column(db.String(30))
    seventh_grade_afternoon_end = db.Column(db.String(30))

    eight_grade_morning_start = db.Column(db.String(30))
    eight_grade_morning_end = db.Column(db.String(30))
    eight_grade_afternoon_start = db.Column(db.String(30))
    eight_grade_afternoon_end = db.Column(db.String(30))

    ninth_grade_morning_start = db.Column(db.String(30))
    ninth_grade_morning_end = db.Column(db.String(30))
    ninth_grade_afternoon_start = db.Column(db.String(30))
    ninth_grade_afternoon_end = db.Column(db.String(30))

    tenth_grade_morning_start = db.Column(db.String(30))
    tenth_grade_morning_end = db.Column(db.String(30))
    tenth_grade_afternoon_start = db.Column(db.String(30))
    tenth_grade_afternoon_end = db.Column(db.String(30))

    eleventh_grade_morning_start = db.Column(db.String(30))
    eleventh_grade_morning_end = db.Column(db.String(30))
    eleventh_grade_afternoon_start = db.Column(db.String(30))
    eleventh_grade_afternoon_end = db.Column(db.String(30))

    twelfth_grade_morning_start = db.Column(db.String(30))
    twelfth_grade_morning_end = db.Column(db.String(30))
    twelfth_grade_afternoon_start = db.Column(db.String(30))
    twelfth_grade_afternoon_end = db.Column(db.String(30))

class Regular(db.Model, Serializer):
    __public__= [
        'school_no',
        'day',
        'junior_kinder_morning_class',
        'junior_kinder_afternoon_class',
        'senior_kinder_morning_class',
        'senior_kinder_afternoon_class',
        'first_grade_morning_class',
        'first_grade_afternoon_class',
        'second_grade_morning_class',
        'second_grade_afternoon_class',
        'third_grade_morning_class',
        'third_grade_afternoon_class',
        'fourth_grade_morning_class',
        'fourth_grade_afternoon_class',
        'fifth_grade_morning_class',
        'fifth_grade_afternoon_class',
        'sixth_grade_morning_class',
        'sixth_grade_afternoon_class',
        'seventh_grade_morning_class',
        'seventh_grade_afternoon_class',
        'eight_grade_morning_class',
        'eight_grade_afternoon_class',
        'ninth_grade_morning_class',
        'ninth_grade_afternoon_class',
        'tenth_grade_morning_class',
        'tenth_grade_afternoon_class',
        'eleventh_grade_morning_class',
        'eleventh_grade_afternoon_class',
        'twelfth_grade_morning_class',
        'twelfth_grade_afternoon_class',
        'junior_kinder_morning_start',
        'junior_kinder_morning_end',
        'junior_kinder_afternoon_start',
        'junior_kinder_afternoon_end',
        'senior_kinder_morning_start',
        'senior_kinder_morning_end',
        'senior_kinder_afternoon_start',
        'senior_kinder_afternoon_end',
        'first_grade_morning_start',
        'first_grade_morning_end',
        'first_grade_afternoon_start',
        'first_grade_afternoon_end',
        'second_grade_morning_start',
        'second_grade_morning_end',
        'second_grade_afternoon_start',
        'second_grade_afternoon_end',
        'third_grade_morning_start',
        'third_grade_morning_end',
        'third_grade_afternoon_start',
        'third_grade_afternoon_end',
        'fourth_grade_morning_start',
        'fourth_grade_morning_end',
        'fourth_grade_afternoon_start',
        'fourth_grade_afternoon_end',
        'fifth_grade_morning_start',
        'fifth_grade_morning_end',
        'fifth_grade_afternoon_start',
        'fifth_grade_afternoon_end',
        'sixth_grade_morning_start',
        'sixth_grade_morning_end',
        'sixth_grade_afternoon_start',
        'sixth_grade_afternoon_end',
        'seventh_grade_morning_start',
        'seventh_grade_morning_end',
        'seventh_grade_afternoon_start',
        'seventh_grade_afternoon_end',
        'eight_grade_morning_start',
        'eight_grade_morning_end',
        'eight_grade_afternoon_start',
        'eight_grade_afternoon_end',
        'ninth_grade_morning_start',
        'ninth_grade_morning_end',
        'ninth_grade_afternoon_start',
        'ninth_grade_afternoon_end',
        'tenth_grade_morning_start',
        'tenth_grade_morning_end',
        'tenth_grade_afternoon_start',
        'tenth_grade_afternoon_end',
        'eleventh_grade_morning_start',
        'eleventh_grade_morning_end',
        'eleventh_grade_afternoon_start',
        'eleventh_grade_afternoon_end',
        'twelfth_grade_morning_start',
        'twelfth_grade_morning_end',
        'twelfth_grade_afternoon_start',
        'twelfth_grade_afternoon_end',
    ]
    id = db.Column(db.Integer, primary_key=True)
    school_no = db.Column(db.String(32))
    day = db.Column(db.String(20))
    junior_kinder_morning_class = db.Column(Boolean, unique=False)
    junior_kinder_afternoon_class = db.Column(Boolean, unique=False)
    senior_kinder_morning_class = db.Column(Boolean, unique=False)
    senior_kinder_afternoon_class = db.Column(Boolean, unique=False)
    first_grade_morning_class = db.Column(Boolean, unique=False)
    first_grade_afternoon_class = db.Column(Boolean, unique=False)
    second_grade_morning_class = db.Column(Boolean, unique=False)
    second_grade_afternoon_class = db.Column(Boolean, unique=False)
    third_grade_morning_class = db.Column(Boolean, unique=False)
    third_grade_afternoon_class = db.Column(Boolean, unique=False)
    fourth_grade_morning_class = db.Column(Boolean, unique=False)
    fourth_grade_afternoon_class = db.Column(Boolean, unique=False)
    fifth_grade_morning_class = db.Column(Boolean, unique=False)
    fifth_grade_afternoon_class = db.Column(Boolean, unique=False)
    sixth_grade_morning_class = db.Column(Boolean, unique=False)
    sixth_grade_afternoon_class = db.Column(Boolean, unique=False)
    seventh_grade_morning_class = db.Column(Boolean, unique=False)
    seventh_grade_afternoon_class = db.Column(Boolean, unique=False)
    eight_grade_morning_class = db.Column(Boolean, unique=False)
    eight_grade_afternoon_class = db.Column(Boolean, unique=False)
    ninth_grade_morning_class = db.Column(Boolean, unique=False)
    ninth_grade_afternoon_class = db.Column(Boolean, unique=False)
    tenth_grade_morning_class = db.Column(Boolean, unique=False)
    tenth_grade_afternoon_class = db.Column(Boolean, unique=False)
    eleventh_grade_morning_class = db.Column(Boolean, unique=False)
    eleventh_grade_afternoon_class = db.Column(Boolean, unique=False)
    twelfth_grade_morning_class = db.Column(Boolean, unique=False)
    twelfth_grade_afternoon_class = db.Column(Boolean, unique=False)

    junior_kinder_morning_start = db.Column(db.String(30))
    junior_kinder_morning_end = db.Column(db.String(30))
    junior_kinder_afternoon_start = db.Column(db.String(30))
    junior_kinder_afternoon_end = db.Column(db.String(30))
    senior_kinder_morning_start = db.Column(db.String(30))
    senior_kinder_morning_end = db.Column(db.String(30))
    senior_kinder_afternoon_start = db.Column(db.String(30))
    senior_kinder_afternoon_end = db.Column(db.String(30))
    first_grade_morning_start = db.Column(db.String(30))
    first_grade_morning_end = db.Column(db.String(30))
    first_grade_afternoon_start = db.Column(db.String(30))
    first_grade_afternoon_end = db.Column(db.String(30))
    second_grade_morning_start = db.Column(db.String(30))
    second_grade_morning_end = db.Column(db.String(30))
    second_grade_afternoon_start = db.Column(db.String(30))
    second_grade_afternoon_end = db.Column(db.String(30))

    third_grade_morning_start = db.Column(db.String(30))
    third_grade_morning_end = db.Column(db.String(30))
    third_grade_afternoon_start = db.Column(db.String(30))
    third_grade_afternoon_end = db.Column(db.String(30))

    fourth_grade_morning_start = db.Column(db.String(30))
    fourth_grade_morning_end = db.Column(db.String(30))
    fourth_grade_afternoon_start = db.Column(db.String(30))
    fourth_grade_afternoon_end = db.Column(db.String(30))

    fifth_grade_morning_start = db.Column(db.String(30))
    fifth_grade_morning_end = db.Column(db.String(30))
    fifth_grade_afternoon_start = db.Column(db.String(30))
    fifth_grade_afternoon_end = db.Column(db.String(30))

    sixth_grade_morning_start = db.Column(db.String(30))
    sixth_grade_morning_end = db.Column(db.String(30))
    sixth_grade_afternoon_start = db.Column(db.String(30))
    sixth_grade_afternoon_end = db.Column(db.String(30))

    seventh_grade_morning_start = db.Column(db.String(30))
    seventh_grade_morning_end = db.Column(db.String(30))
    seventh_grade_afternoon_start = db.Column(db.String(30))
    seventh_grade_afternoon_end = db.Column(db.String(30))

    eight_grade_morning_start = db.Column(db.String(30))
    eight_grade_morning_end = db.Column(db.String(30))
    eight_grade_afternoon_start = db.Column(db.String(30))
    eight_grade_afternoon_end = db.Column(db.String(30))

    ninth_grade_morning_start = db.Column(db.String(30))
    ninth_grade_morning_end = db.Column(db.String(30))
    ninth_grade_afternoon_start = db.Column(db.String(30))
    ninth_grade_afternoon_end = db.Column(db.String(30))

    tenth_grade_morning_start = db.Column(db.String(30))
    tenth_grade_morning_end = db.Column(db.String(30))
    tenth_grade_afternoon_start = db.Column(db.String(30))
    tenth_grade_afternoon_end = db.Column(db.String(30))

    eleventh_grade_morning_start = db.Column(db.String(30))
    eleventh_grade_morning_end = db.Column(db.String(30))
    eleventh_grade_afternoon_start = db.Column(db.String(30))
    eleventh_grade_afternoon_end = db.Column(db.String(30))

    twelfth_grade_morning_start = db.Column(db.String(30))
    twelfth_grade_morning_end = db.Column(db.String(30))
    twelfth_grade_afternoon_start = db.Column(db.String(30))
    twelfth_grade_afternoon_end = db.Column(db.String(30))