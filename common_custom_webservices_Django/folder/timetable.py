import psycopg2
from flask import Flask, request,send_file
exp_time = ""
app = Flask(__name__)
from datetime import datetime,date
import time,requests,datetime as date,pytz
import calendar
from dateutil.relativedelta import relativedelta
from flask import Flask, request ,send_from_directory, render_template,make_response,jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

api = Api(app)
CORS(app)


resp = requests.get(url='http://localhost:5000/get_db_config',params=None)
print(resp)
data = resp.json()
print(data)
result = data['Results']
database = result['database']
print(database)


conned = psycopg2.connect(host="localhost", database=database, port="5432", user="openpg", password="openpgpwd")
cursored = conned.cursor()


def checkColumnExists():
cursored.execute("select count(*)column_name from information_schema.columns where table_name='op_session'"
"and column_name in ('notes','title')")
column_names = cursored.fetchone()
print(column_names)
if 2 != column_names[0]:
cursored.execute("alter table op_session ADD COLUMN notes character varying,"
"ADD COLUMN title character varying")
conned.commit()
return True
else:
print("Notes,Title column is already exists")
return True


@app.route('/get_timetable', methods=['GET','POST'])
def get_timetable():
print('TIMETABLE')
checkColumnExists()
req_data = request.get_json()
course_id = req_data['course_id']
batch_id = req_data['batch_id']
query1 = """select A.course_id,B.name as course_name,A.batch_id,C.name as batch_name,
A.start_datetime,A.end_datetime,A.type
from op_session A join op_course B on A.course_id=B.id
join op_batch C on A.batch_id=C.id where A.course_id='%s' and A.batch_id='%s'"""\
%(course_id,batch_id)
cursored.execute(query1)
mycheck1 = cursored.fetchall()
course = ''
for row1 in mycheck1:
if course == '':
course += str(row1[1])
elif str(row1[1]) not in course:
course += ','
course += str(row1[1])
li = course
courses = li.split(',')
print(courses)
batch = ''
for row2 in mycheck1:
if batch == '':
batch += str(row2[3])
elif str(row2[3]) not in batch:
batch += ','
batch += str(row2[3])
li = batch
batchs = li.split(',')
print(batchs)
conned.commit()
final_timetable_docs_report = []
sl_no1 = 0
for cour in courses:
for batc in batchs:
sl_no1 += 1
val = {
'sl_no': sl_no1,
# "course_id": cour[1],
"course_name": cour,
# "batch_id": batc[1],
"batch_name": batc,
"period": ""
}
query2 = """select A.course_id,B.name as course_name,A.batch_id,C.name as batch_name,
A.start_datetime,A.end_datetime,A.type
from op_session A join op_course B on A.course_id=B.id
join op_batch C on A.batch_id=C.id where A.course_id='%s' and A.batch_id='%s'""" \
% (course_id, batch_id)
cursored.execute(query2)
mycheck2 = cursored.fetchall()
day = ''
for day1 in mycheck2:
if day == '':
day += str(day1[6])
elif str(day1[6]) not in day:
day += ','
day += str(day1[6])
li = day
days = li.split(',')
print(days)
sl_no2 = 0
period_val = []
for row3 in days:
query1 = """select A.id as session_id
from op_session A join op_course B on A.course_id=B.id
join op_batch C on A.batch_id=C.id where B.name='%s' and C.name='%s' and A.type='%s'""" \
% (cour, batc,row3)
cursored.execute(query1)
session = cursored.fetchall()
if session == []:
session_val = ''
else:
session_val = session[0][0]
sl_no2 += 1
val2 = {
'sl_no': sl_no2,
# "session_id": session_val,
"day": row3,
"timing": ""
}
period_val.append(val2)
query4 = """select A.course_id,B.name as course_name,A.batch_id,C.name as batch_name,
A.start_datetime,A.end_datetime,A.type,D.name as timing,F.name as faculty_name,
A.subject_id,A.id,G.name as subject_name,A.name as session_name
from op_session A join op_course B on A.course_id=B.id
join op_batch C on A.batch_id=C.id
join op_timing D on D.id=A.timing_id
join op_faculty E on E.id=A.faculty_id join res_partner F on F.id=E.partner_id
join op_subject G on G.id=A.subject_id
where A.course_id='%s' and A.batch_id='%s'
and A.type='%s'""" \
% (course_id, batch_id,row3)
cursored.execute(query4)
mycheck4 = cursored.fetchall()
timing = []
sl_no3 = 0
for row4 in mycheck4:
query5 = """select H.name
from op_session A join op_course B on A.course_id=B.id
join op_batch C on A.batch_id=C.id
join op_timing D on D.id=A.timing_id
join op_faculty E on E.id=A.faculty_id join res_partner F on F.id=E.partner_id
join op_subject G on G.id=A.subject_id join op_activity_type H on H.id=A.activity_id
where A.course_id='%s' and A.batch_id='%s' and A.type='%s' and A.subject_id='%s' and A.id='%s'""" \
% (course_id, batch_id, row3, row4[9], row4[10])
cursored.execute(query5)
mycheck5 = cursored.fetchall()
activity = ''
if mycheck5 != None:
for row5 in mycheck5:
activity = str(row5[0])
query6 = """select H.name
from op_session A join op_course B on A.course_id=B.id
join op_batch C on A.batch_id=C.id
join op_timing D on D.id=A.timing_id
join op_faculty E on E.id=A.faculty_id join res_partner F on F.id=E.partner_id
join op_subject G on G.id=A.subject_id join op_classroom H on H.id=A.classroom_id
where A.course_id='%s' and A.batch_id='%s' and A.type='%s' and A.subject_id='%s' and A.id='%s'""" \
% (course_id, batch_id, row3, row4[9], row4[10])
cursored.execute(query6)
mycheck6 = cursored.fetchall()
classroom = ''
if mycheck6 != None:
for row6 in mycheck6:
classroom = str(row6[0])
sl_no3 += 1
start_datetime = row4[4]
end_datetime = row4[5]
hours = 5
minutes = 30
seconds = 00
d = date.timedelta(hours=hours, minutes=minutes, seconds=seconds)
sdate = start_datetime + d
edate = end_datetime + d
start_date = sdate.strftime("%a, %d %b %Y %H:%M:%S")
end_date = edate.strftime("%a, %d %b %Y %H:%M:%S")
val3 = {
'sl_no': sl_no3,
'session_id': row4[10],
'session_name': row4[12],
'timing': row4[7],
'faculty_name': row4[8],
'subject_name': row4[11],
'start_date': start_date,
'end_date': end_date,
'chapter': "",
'lesson': "",
'activity_name': activity,
'classroom_name': classroom
}
timing.append(val3)
query7 = """select I.chapter_name chapter_name,H.op_chapter_id,A.id
from op_session A join op_course B on A.course_id=B.id
join op_batch C on A.batch_id=C.id
join op_timing D on D.id=A.timing_id
join op_faculty E on E.id=A.faculty_id join res_partner F on F.id=E.partner_id
join op_subject G on G.id=A.subject_id
join op_chapter_op_session_rel H on H.op_session_id=A.id
join op_chapter I on I.id=H.op_chapter_id
where A.course_id='%s' and A.batch_id='%s' and A.type='%s' and A.subject_id='%s' and
H.op_session_id='%s'""" \
% (course_id, batch_id, row3, row4[9],row4[10])
cursored.execute(query7)
mycheck7 = cursored.fetchall()
chapter = []
sl_no4 = 0
for row7 in mycheck7:
sl_no4 += 1
val4 = {
'sl_no': sl_no4,
'chapter_name': row7[0]
}
chapter.append(val4)
query8 = """select K.lesson_name,J.op_lesson_id,A.id
from op_session A join op_course B on A.course_id=B.id
join op_batch C on A.batch_id=C.id
join op_timing D on D.id=A.timing_id
join op_faculty E on E.id=A.faculty_id join res_partner F on F.id=E.partner_id
join op_subject G on G.id=A.subject_id
join op_chapter_op_session_rel H on H.op_session_id=A.id
join op_chapter I on I.id=H.op_chapter_id
join op_lesson_op_session_rel J on J.op_session_id = A.id
join op_lesson K on K.id=J.op_lesson_id
where A.course_id='%s' and A.batch_id='%s' and A.type='%s' and A.subject_id='%s'
and H.op_chapter_id='%s' and J.op_session_id='%s'""" \
% (course_id, batch_id, row3, row4[9],row7[1],row7[2])
cursored.execute(query8)
mycheck8 = cursored.fetchall()
lesson = []
sl_no5 = 0
for row5 in mycheck8:
sl_no5 += 1
val5 = {
'sl_no': sl_no5,
'lesson_name': row5[0]
}
lesson.append(val5)
val3['lesson'] = lesson
val3['chapter'] = chapter
val2['timing'] = timing
val['period'] = period_val
final_timetable_docs_report.append(val)
output_msg = {"results": final_timetable_docs_report}
print(output_msg)
return jsonify(output_msg)
import psycopg2
from flask import Flask, request
exp_time = ""
app = Flask(__name__)
from datetime import datetime,date
import time
import calendar
import requests,json
from dateutil.relativedelta import relativedelta
from flask import Flask, request ,send_from_directory, render_template,make_response,jsonify
# conn = ""
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from passlib.context import CryptContext
import os,yaml
current_directory = os.path.dirname(os.getcwd())
path = current_directory+'/edmaster_config.yml'
print(path)
api = Api(app)
CORS(app)
}


