from celery import Celery
import db_conn
from db_conn import db
from models import *
import requests
import uuid

app = Celery('tasks', broker='amqp://sgb:sgbsaints@rabbitmq/pisara')

SMS_NOTIFICATION_URL = 'https://post.chikka.com/smsapi/request'
CLIENT_ID = 'ef8cf56d44f93b6ee6165a0caa3fe0d1ebeee9b20546998931907edbb266eb72'
SECRET_KEY = 'c4c461cc5aa5f9f89b701bc016a73e9981713be1bf7bb057c875dbfacff86e1d'
SHORT_CODE = '29290420420'
IPP_URL = 'https://devapi.globelabs.com.ph/smsmessaging/v1/outbound/%s/requests'
IPP_SHORT_CODE = 21587460

# os.environ['DATABASE_URL']
# 'postgresql://admin:sgbsaints@db/sgb'
# 'sqlite:///local.db'

@app.task
def send_message(log_id, type, message, msisdn, action):
    log = Log.query.filter_by(id=log_id).first()

    # message_options = {
    #         "message": message,
    #         "address": msisdn,
    #         "access_token": 'Os-vcHVaxj6yQrjefuU4Z20tIkzyHxXom_AvK1GfLl0'
    #     }

    # try:
    #     r = requests.post(
    #     IPP_URL % IPP_SHORT_CODE,
    #     params=message_options
    #     )
    #     print r.status_code
    #     print r.text
    #     return

    # except requests.exceptions.ConnectionError as e:
    #     print "Sending Failed!"
    #     return

    message_options = {
            'message_type': 'SEND',
            'message': message,
            'client_id': CLIENT_ID,
            'mobile_number': msisdn,
            'secret_key': SECRET_KEY,
            'shortcode': SHORT_CODE,
            'message_id': uuid.uuid4().hex
        }

    try:
        r = requests.post(SMS_NOTIFICATION_URL,message_options)           
        if r.status_code == 200:
            print(str(r.status_code))
            print(str(r.json))
            if action == 'entered':
                log.time_in_notification_status='Success'
            else:
                log.time_out_notification_status='Success'
            db.session.commit()
            return
        if action == 'entered':
            log.time_in_notification_status='Failed'
        else:
            log.time_out_notification_status='Failed'
        db.session.commit()
        print(str(r.status_code))
        return

    except:
        print("Sending Failed!")
        if action == 'entered':
            log.time_in_notification_status='Failed'
        else:
            log.time_out_notification_status='Failed'
        db.session.commit()
        return