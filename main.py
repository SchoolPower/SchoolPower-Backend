from bs4 import BeautifulSoup
import login
import config
import requests
import re
import json
import sys
import threading

HOST=config.HOST
URL_HOME=HOST+"home.html"
GRADE_REGEX=re.compile(r"(.*?)if.*write\(\"(.*?)\%")
FIX_REGEX=re.compile(r"<a href=.*?/>")
ROOM_REGEX=re.compile(r"Rm: (.*?)</td>")
COURSE_ID_REGEX=re.compile(r"frn=(\d*?)&")

PERIOD_FILTER=[] if len(sys.argv)<4 else sys.argv[3].split(",")

class Assignment:
    def __init__(self, data):
        while len(data)<7: data.append("")
        self.date,self.category,self.assignment,_,self.score,self.percent,self.grade=data
        
class FetchData(threading.Thread):
    def __init__(self, subject, session, link):
        threading.Thread.__init__(self)
        self.subject=subject
        self.session=session
        self.link=link
        
    def run(self):
        # Get the page
        self.subject.handle(self.session.post(HOST+self.link,timeout=10).text)
        
class Subject:
    def __init__(self, session, link, room):
        self.room=room
        self.term=link[-2:]
        self.thread=FetchData(self, session, link)
        self.thread.start()
        
    def handle(self, html):
        html=FIX_REGEX.sub("<a>",html) # to fix a bug in powerschool
        soup=BeautifulSoup(html,"html.parser")
        
        # Fetch basic information
        self.name,self.teacher,self.block,self.grade=[ele.text for ele in soup.find("table",class_="linkDescList").find_all("td")]
        self.grade,self.mark=GRADE_REGEX.findall(self.grade.replace(" ","").replace("\n","").replace("\xa0",""))[0]
        
        # Fetch Assignments
        table_assignments=soup.find("h2").next.next.next
        self.assignments=[]
        for row in table_assignments.find_all("tr"):
            if row.find_all("th"): continue
            self.assignments.append(Assignment([ele.text for ele in row.find_all("td")][:7]))
        
    def wait_for_data(self):
        self.thread.join()
        del self.thread
        

def get_subjects(session):
    subjects=[]
    html=session.get(URL_HOME,timeout=10).text
    html=html.replace("按课程划分的出勤</th></tr>","") # fix the bug in mandarin chinese version
    
    # Find Room#
    rooms=ROOM_REGEX.findall(html)
    
    soup=BeautifulSoup(html,"html.parser")
    
    # Print student's name
    print(soup.find('li',id="userName").find('span').text.strip())
    
    # Find the links to courses
    i=-1
    old_id=0
    for link in soup.find('table',class_="grid").find_all('a'):
        if link.text=="--": continue
        href=link["href"]
        if href[:5]!="score": continue
        id=COURSE_ID_REGEX.search(href).group()
        if id!=old_id: i+=1
        old_id=id
        if not href[-2:] in PERIOD_FILTER and len(PERIOD_FILTER)>0: continue
        subjects.append(Subject(session, href, rooms[i]))
    return subjects
    
try:
    session=login.login(sys.argv[1],sys.argv[2])
except login.WrongPasswordError:
    print('{"error":1,"description":"Invalid username or password."}')
    exit(0)
subjects=get_subjects(session)
for subject in subjects:
    subject.wait_for_data()
    
print(json.dumps(subjects, default=(lambda obj:obj.__dict__)))
