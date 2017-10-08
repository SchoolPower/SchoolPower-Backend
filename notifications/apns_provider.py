from apns2.client import APNsClient
from apns2.payload import Payload
import pymysql
import time

DATA_UPDATE_URL = "https://127.0.0.1:8443/api/2.0/get_data.php"
TOPIC = 'studio.schoolpower.SchoolPower'
PEM_FILE_PATH = 'apns.pem'
SQL_SERVER_ADDRESS = "127.0.0.1"
SQL_SERVER_USER = "root"
SQL_SERVER_PASSWORD = ""
SQL_SERVER_DATABASE = "schoolpower"

def process_user(token, username, password, invalid_list):
    try:
        token_hex = ''
        payload = Payload(content_available=1, custom={'subject_data': requests.post(DATA_UPDATE_URL, data={"username": username, "password": password}).text})
        
        client = APNsClient(PEM_FILE_PATH, use_sandbox=True, use_alternative_port=False)
        client.send_notification(token_hex, payload, TOPIC)
    except BadDeviceToken:
        invalid_list.append(token)

time_start=time.time()

db = pymysql.connect(SQL_SERVER_ADDRESS, SQL_SERVER_USER, SQL_SERVER_PASSWORD, SQL_SERVER_DATABASE)

cursor = db.cursor()

cursor.execute("SELECT * FROM apns")
results = cursor.fetchall()
invalid_list = []

for row in results:
    token, username, password = row[1], row[2], row[3]
    process_user(token, username, password, invalid_list)

for token in invalid_list:
    cursor.execute("DELETE FROM apns WHERE token = '%s'"%token)

db.close()

print("Notification Pushed. %d valid devices. $d devices are removed."%(len(result),len(token)))
print("Time Used = %ds"%(time.time()-time_start))
