import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from base64 import b64encode
from hashlib import md5
from bs4 import BeautifulSoup
import hmac
import config

HOST=config.HOST
URL_HOME=HOST+"home.html"

class WrongPasswordError(Exception):
    pass
    
def hex_hmac_md5(key, code):
    return hmac.new(key, code).hexdigest()

# login. Return: requests.Session
def login(username,password):
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=Retry(total=5,backoff_factor=0.5)))
    # try to open the index page
    soup=BeautifulSoup(session.get(URL_HOME).text,"html.parser")

    pstoken = soup.find('input',attrs={'name':'pstoken'})["value"]
    pskey = soup.find('input',attrs={'name':'contextData'})["value"].encode()

    b64pw=b64encode(md5(password.encode()).digest()).replace(b'=', b'A')[:-2]

    pw=hex_hmac_md5(pskey,b64pw)
    dbpw=hex_hmac_md5(pskey,password.encode())

    return_page=session.post(URL_HOME, params={
    'pstoken':pstoken,'contextData':pskey,'dbpw':dbpw,
    'serviceName':'PS Parent Portal','pcasServerUrl':'/',
    'credentialType':'User Id and Password Credential',
    'request_locale':'zh_CN','account':username,'pw':pw,
    'translator_username':'','translator_password':'',
    'translator_ldappassword':'','serviceTicket':'',
    'translatorpw':''}).text
    
    if "Login" in return_page:
        raise WrongPasswordError()
    
    return session