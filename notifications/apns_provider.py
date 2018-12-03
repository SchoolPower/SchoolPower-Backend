from apns2.client import APNsClient
from apns2.payload import Payload
from apns2.errors import BadDeviceToken
from apns2.errors import Unregistered
import pymysql
import time
import requests
import config
import datetime

TOPIC = 'studio.schoolpower.SchoolPower'
PEM_FILE_PATH = 'apns.pem'

client = APNsClient(PEM_FILE_PATH, use_sandbox=False, use_alternative_port=False)

time_start=time.time()

db = pymysql.connect(config.SQL_SERVER_ADDRESS, config.SQL_SERVER_USER, config.SQL_SERVER_PASSWORD, config.SQL_SERVER_DATABASE)

cursor = db.cursor()

cursor.execute("SELECT * FROM apns")
results = list(set(cursor.fetchall()))
invalid_list = []
for row in results:
    token_id = row[0]
    token = row[1]
    try:
        client.send_notification(token, Payload(content_available=1), TOPIC)
        time.sleep(0.08)
    except BadDeviceToken:
        invalid_list.append(token_id)
    except Unregistered:
        invalid_list.append(token_id)
for token_id in invalid_list:
    cursor.execute("DELETE FROM apns WHERE id = %d" % int(token_id))

db.commit()
db.close()
f = open("log","a")
f.write(str(datetime.datetime.now()))
f.write("\nNotification Pushed. %d devices. %d devices are removed.\n"%(len(results),len(invalid_list)))
f.write("Time Used = %ds\n"%(time.time()-time_start))
