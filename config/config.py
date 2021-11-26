import os
import sys

TOPIC = 'studio.schoolpower.SchoolPower'
PS_API = 'https://powerschool.mapleleaf.cn'
CACHE_DB_LOCATION = os.environ.get("CACHE_DB_LOCATION", None)
DB_LOCATION = os.environ.get('DB_LOCATION', 'users.db')
PEM_FILE_PATH = os.environ.get("APNS_CERT_FILE", None)
SECRET = os.environ.get("SECRET", "test")

if SECRET == "test":
    print("SECRET not set. Make sure you set it when it's deployed.", file=sys.stderr)
