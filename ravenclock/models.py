import flask, flask.views
from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean
import helpers.db_conn as db
import json

app = flask.Flask(__name__)
db = db.alchemy

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


    def serialize(self):
        return {
        'id': self.id,
        'school_no': self.school_no,
        'date': self.date,
        'dau': self.day,
        'month': self.month,
        'year': self.year,

        'junior_kinder_morning_class': self.junior_kinder_morning_class,
        'junior_kinder_afternoon_class': self.junior_kinder_afternoon_class,
        'senior_kinder_morning_class': self.senior_kinder_afternoon_class,
        'senior_kinder_afternoon_class': self.senior_kinder_afternoon_class,
        'first_grade_morning_class': self.first_grade_morning_class,
        'first_grade_afternoon_class': self.first_grade_afternoon_class,
        'second_grade_morning_class': self.second_grade_morning_class,
        'second_grade_afternoon_class': self.second_grade_afternoon_class,
        'third_grade_morning_class': self.third_grade_morning_class,
        'third_grade_afternoon_class': self.third_grade_afternoon_class,
        'fourth_grade_morning_class': self.fourth_grade_afternoon_class,
        'fourth_grade_afternoon_class': self.fourth_grade_afternoon_class,
        'fifth_grade_morning_class': self.fifth_grade_afternoon_class,
        'fifth_grade_afternoon_class': self.fifth_grade_afternoon_class,
        'sixth_grade_morning_class': self.sixth_grade_afternoon_class,
        'sixth_grade_afternoon_class': self.sixth_grade_afternoon_class,
        'seventh_grade_morning_class': self.seventh_grade_afternoon_class,
        'seventh_grade_afternoon_class': self.seventh_grade_afternoon_class,
        'eight_grade_morning_class': self.eight_grade_afternoon_class,
        'eight_grade_afternoon_class': self.eight_grade_afternoon_class,
        'ninth_grade_morning_class': self.ninth_grade_afternoon_class,
        'ninth_grade_afternoon_class': self.ninth_grade_afternoon_class,
        'tenth_grade_morning_class': self.tenth_grade_afternoon_class,
        'tenth_grade_afternoon_class': self.tenth_grade_afternoon_class,
        'eleventh_grade_morning_class': self.eleventh_grade_afternoon_class,
        'eleventh_grade_afternoon_class': self.eleventh_grade_afternoon_class,
        'twelfth_grade_morning_class': self.twelfth_grade_afternoon_class,
        'twelfth_grade_afternoon_class': self.twelfth_grade_afternoon_class,
        'junior_kinder_morning_start': self.junior_kinder_morning_start,
        'junior_kinder_morning_end': self.junior_kinder_morning_end,
        'junior_kinder_afternoon_start': self.junior_kinder_afternoon_start,
        'junior_kinder_afternoon_end': self.junior_kinder_afternoon_end,
        'senior_kinder_morning_start': self.senior_kinder_morning_start,
        'senior_kinder_morning_end': self.senior_kinder_morning_end,
        'senior_kinder_afternoon_start': self.senior_kinder_afternoon_start,
        'senior_kinder_afternoon_end': self.senior_kinder_afternoon_end,
        'first_grade_morning_start': self.first_grade_morning_start,
        'first_grade_morning_end': self.first_grade_morning_end,
        'first_grade_afternoon_start': self.first_grade_afternoon_start,
        'first_grade_afternoon_end': self.first_grade_afternoon_end,
        'second_grade_morning_start': self.second_grade_morning_start,
        'second_grade_morning_end': self.second_grade_morning_end,
        'second_grade_afternoon_start': self.second_grade_afternoon_start,
        'second_grade_afternoon_end': self.second_grade_afternoon_end,
        'third_grade_morning_start': self.third_grade_morning_start,
        'third_grade_morning_end': self.third_grade_morning_end,
        'third_grade_afternoon_start': self.third_grade_afternoon_start,
        'third_grade_afternoon_end': self.third_grade_afternoon_end,
        'fourth_grade_morning_start': self.fourth_grade_morning_start,
        'fourth_grade_morning_end': self.fourth_grade_morning_end,
        'fourth_grade_afternoon_start': self.fourth_grade_afternoon_start,
        'fourth_grade_afternoon_end': self.fourth_grade_afternoon_end,
        'fifth_grade_morning_start': self.fifth_grade_morning_start,
        'fifth_grade_morning_end': self.fifth_grade_morning_end,
        'fifth_grade_afternoon_start': self.fifth_grade_afternoon_start,
        'fifth_grade_afternoon_end': self.fifth_grade_afternoon_end,
        'sixth_grade_morning_start': self.sixth_grade_morning_start,
        'sixth_grade_morning_end': self.sixth_grade_morning_end,
        'sixth_grade_afternoon_start': self.sixth_grade_afternoon_start,
        'sixth_grade_afternoon_end': self.sixth_grade_afternoon_end,
        'seventh_grade_morning_start': self.seventh_grade_morning_start,
        'seventh_grade_morning_end': self.seventh_grade_morning_end,
        'seventh_grade_afternoon_start': self.seventh_grade_afternoon_start,
        'seventh_grade_afternoon_end': self.seventh_grade_afternoon_end,
        'eight_grade_morning_start': self.eight_grade_morning_start,
        'eight_grade_morning_end': self.eight_grade_morning_end,
        'eight_grade_afternoon_start': self.eight_grade_afternoon_start,
        'eight_grade_afternoon_end': self.eight_grade_afternoon_end,
        'ninth_grade_morning_start': self.ninth_grade_morning_start,
        'ninth_grade_morning_end': self.ninth_grade_morning_end,
        'ninth_grade_afternoon_start': self.ninth_grade_afternoon_start,
        'ninth_grade_afternoon_end': self.ninth_grade_afternoon_end,
        'tenth_grade_morning_start': self.tenth_grade_morning_start,
        'tenth_grade_morning_end': self.tenth_grade_morning_end,
        'tenth_grade_afternoon_start': self.tenth_grade_afternoon_start,
        'tenth_grade_afternoon_end': self.tenth_grade_afternoon_end,
        'eleventh_grade_morning_start': self.eleventh_grade_morning_start,
        'eleventh_grade_morning_end': self.eleventh_grade_morning_end,
        'eleventh_grade_afternoon_start': self.eleventh_grade_afternoon_start,
        'eleventh_grade_afternoon_end': self.eleventh_grade_afternoon_end,
        'twelfth_grade_morning_start': self.twelfth_grade_morning_start,
        'twelfth_grade_morning_end': self.twelfth_grade_morning_end,
        'twelfth_grade_afternoon_start': self.twelfth_grade_afternoon_start,
        'twelfth_grade_afternoon_end': self.twelfth_grade_afternoon_end
        }

class Regular(db.Model,Serializer):
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

    def serialize(self):
        return {
        'id': self.id,
        'school_no': self.school_no,
        'day': self.day,

        'junior_kinder_morning_class': self.junior_kinder_morning_class,
        'junior_kinder_afternoon_class': self.junior_kinder_afternoon_class,
        'senior_kinder_morning_class': self.senior_kinder_afternoon_class,
        'senior_kinder_afternoon_class': self.senior_kinder_afternoon_class,
        'first_grade_morning_class': self.first_grade_morning_class,
        'first_grade_afternoon_class': self.first_grade_afternoon_class,
        'second_grade_morning_class': self.second_grade_morning_class,
        'second_grade_afternoon_class': self.second_grade_afternoon_class,
        'third_grade_morning_class': self.third_grade_morning_class,
        'third_grade_afternoon_class': self.third_grade_afternoon_class,
        'fourth_grade_morning_class': self.fourth_grade_afternoon_class,
        'fourth_grade_afternoon_class': self.fourth_grade_afternoon_class,
        'fifth_grade_morning_class': self.fifth_grade_afternoon_class,
        'fifth_grade_afternoon_class': self.fifth_grade_afternoon_class,
        'sixth_grade_morning_class': self.sixth_grade_afternoon_class,
        'sixth_grade_afternoon_class': self.sixth_grade_afternoon_class,
        'seventh_grade_morning_class': self.seventh_grade_afternoon_class,
        'seventh_grade_afternoon_class': self.seventh_grade_afternoon_class,
        'eight_grade_morning_class': self.eight_grade_afternoon_class,
        'eight_grade_afternoon_class': self.eight_grade_afternoon_class,
        'ninth_grade_morning_class': self.ninth_grade_afternoon_class,
        'ninth_grade_afternoon_class': self.ninth_grade_afternoon_class,
        'tenth_grade_morning_class': self.tenth_grade_afternoon_class,
        'tenth_grade_afternoon_class': self.tenth_grade_afternoon_class,
        'eleventh_grade_morning_class': self.eleventh_grade_afternoon_class,
        'eleventh_grade_afternoon_class': self.eleventh_grade_afternoon_class,
        'twelfth_grade_morning_class': self.twelfth_grade_afternoon_class,
        'twelfth_grade_afternoon_class': self.twelfth_grade_afternoon_class,
        'junior_kinder_morning_start': self.junior_kinder_morning_start,
        'junior_kinder_morning_end': self.junior_kinder_morning_end,
        'junior_kinder_afternoon_start': self.junior_kinder_afternoon_start,
        'junior_kinder_afternoon_end': self.junior_kinder_afternoon_end,
        'senior_kinder_morning_start': self.senior_kinder_morning_start,
        'senior_kinder_morning_end': self.senior_kinder_morning_end,
        'senior_kinder_afternoon_start': self.senior_kinder_afternoon_start,
        'senior_kinder_afternoon_end': self.senior_kinder_afternoon_end,
        'first_grade_morning_start': self.first_grade_morning_start,
        'first_grade_morning_end': self.first_grade_morning_end,
        'first_grade_afternoon_start': self.first_grade_afternoon_start,
        'first_grade_afternoon_end': self.first_grade_afternoon_end,
        'second_grade_morning_start': self.second_grade_morning_start,
        'second_grade_morning_end': self.second_grade_morning_end,
        'second_grade_afternoon_start': self.second_grade_afternoon_start,
        'second_grade_afternoon_end': self.second_grade_afternoon_end,
        'third_grade_morning_start': self.third_grade_morning_start,
        'third_grade_morning_end': self.third_grade_morning_end,
        'third_grade_afternoon_start': self.third_grade_afternoon_start,
        'third_grade_afternoon_end': self.third_grade_afternoon_end,
        'fourth_grade_morning_start': self.fourth_grade_morning_start,
        'fourth_grade_morning_end': self.fourth_grade_morning_end,
        'fourth_grade_afternoon_start': self.fourth_grade_afternoon_start,
        'fourth_grade_afternoon_end': self.fourth_grade_afternoon_end,
        'fifth_grade_morning_start': self.fifth_grade_morning_start,
        'fifth_grade_morning_end': self.fifth_grade_morning_end,
        'fifth_grade_afternoon_start': self.fifth_grade_afternoon_start,
        'fifth_grade_afternoon_end': self.fifth_grade_afternoon_end,
        'sixth_grade_morning_start': self.sixth_grade_morning_start,
        'sixth_grade_morning_end': self.sixth_grade_morning_end,
        'sixth_grade_afternoon_start': self.sixth_grade_afternoon_start,
        'sixth_grade_afternoon_end': self.sixth_grade_afternoon_end,
        'seventh_grade_morning_start': self.seventh_grade_morning_start,
        'seventh_grade_morning_end': self.seventh_grade_morning_end,
        'seventh_grade_afternoon_start': self.seventh_grade_afternoon_start,
        'seventh_grade_afternoon_end': self.seventh_grade_afternoon_end,
        'eight_grade_morning_start': self.eight_grade_morning_start,
        'eight_grade_morning_end': self.eight_grade_morning_end,
        'eight_grade_afternoon_start': self.eight_grade_afternoon_start,
        'eight_grade_afternoon_end': self.eight_grade_afternoon_end,
        'ninth_grade_morning_start': self.ninth_grade_morning_start,
        'ninth_grade_morning_end': self.ninth_grade_morning_end,
        'ninth_grade_afternoon_start': self.ninth_grade_afternoon_start,
        'ninth_grade_afternoon_end': self.ninth_grade_afternoon_end,
        'tenth_grade_morning_start': self.tenth_grade_morning_start,
        'tenth_grade_morning_end': self.tenth_grade_morning_end,
        'tenth_grade_afternoon_start': self.tenth_grade_afternoon_start,
        'tenth_grade_afternoon_end': self.tenth_grade_afternoon_end,
        'eleventh_grade_morning_start': self.eleventh_grade_morning_start,
        'eleventh_grade_morning_end': self.eleventh_grade_morning_end,
        'eleventh_grade_afternoon_start': self.eleventh_grade_afternoon_start,
        'eleventh_grade_afternoon_end': self.eleventh_grade_afternoon_end,
        'twelfth_grade_morning_start': self.twelfth_grade_morning_start,
        'twelfth_grade_morning_end': self.twelfth_grade_morning_end,
        'twelfth_grade_afternoon_start': self.twelfth_grade_afternoon_start,
        'twelfth_grade_afternoon_end': self.twelfth_grade_afternoon_end
        }

class School(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    school_no = db.Column(db.String(32))
    api_key = db.Column(db.String(32))
    name = db.Column(db.String(50))