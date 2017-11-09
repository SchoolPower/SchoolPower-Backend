from apns2.client import APNsClient
from apns2.payload import Payload
from apns2.errors import BadDeviceToken
import pymysql
import time
import requests
import config

TOPIC = 'studio.schoolpower.SchoolPower'
PEM_FILE_PATH = 'apns.pem'

client = APNsClient(PEM_FILE_PATH, use_sandbox=True, use_alternative_port=False)

time_start=time.time()

db = pymysql.connect(config.SQL_SERVER_ADDRESS, config.SQL_SERVER_USER, config.SQL_SERVER_PASSWORD, config.SQL_SERVER_DATABASE)

cursor = db.cursor()

cursor.execute("SELECT * FROM apns")
results = cursor.fetchall()
invalid_list = []
for row in results:
    token = row #[1]
    try:
        client.send_notification(token, Payload(content_available=1), TOPIC)
        time.sleep(1)
    except BadDeviceToken:
        print("bdt")
        invalid_list.append(token)
        
for token in invalid_list:
    cursor.execute("DELETE FROM apns WHERE token = '%s'"%token)

db.commit()
db.close()

print("Notification Pushed. %d devices. %d devices are removed."%(len(results),len(invalid_list)))
print("Time Used = %ds"%(time.time()-time_start))
