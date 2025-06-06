import os
import sys

TOPIC = 'studio.schoolpower.SchoolPower'
PS_API = 'https://ps.mapleleaf.net.cn'
CACHE_DB_LOCATION = os.environ.get("CACHE_DB_LOCATION", None)
DB_LOCATION = os.environ.get('DB_LOCATION', 'users.db')
PEM_FILE_PATH = os.environ.get("APNS_CERT_FILE", None)
SECRET = os.environ.get("SECRET", "test")
TIME_OUT = float(os.environ.get("TIME_OUT", 6))

if SECRET == "test":
    print("SECRET not set. Make sure you set it when it's deployed.", file=sys.stderr)
