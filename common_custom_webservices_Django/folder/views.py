import requests
from django.shortcuts import render
from django.http import HttpResponse, request, response
from django.http import JsonResponse
from .models import op_course
from rest_framework.decorators import api_view
from django.core import serializers
import json
from django.db import connection
import erppeek
import response



# Create your views here.
def index(request):
    print("some thing")
    return render(request,"test/index.html")
@api_view(["GET","POST"])
def get_subject_by_standard(request):
    if request.method =='POST':
        db=json.loads(request.body)
        course_id=db['course_id']
        cursor=connection.cursor()
        query1 = """Select C.id as subject_id,C.name as subject_name from op_course A
            left join op_course_op_subject_rel B on B.op_course_id=A.id
             left join op_subject C on C.id=B.op_subject_id where A.id='%s'"""%(course_id)
        cursor.execute(query1)
        mycheck = [dict(line) for line in [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]
        print({"results": mycheck})
        return JsonResponse({"results": mycheck})
    if request.method =='GET':
        dbs=request.GET
        print(dbs)
        course_id=dbs['course_id']
        cursor=connection.cursor()
        query1 = """Select C.id as subject_id,C.name as subject_name from op_course A
            left join op_course_op_subject_rel B on B.op_course_id=A.id
             left join op_subject C on C.id=B.op_subject_id where A.id='%s'"""%(course_id)
        cursor.execute(query1)
        mycheck = [dict(line) for line in [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]
        print({"results": mycheck})
        return JsonResponse({"results": mycheck})

@api_view(["GET"])
def get_subject(request):
    if request.method == 'GET':
        # dbs=request.GET
        # course_id=dbs['course_id']
        cursor=connection.cursor()
        query1 = """Select id as subject_id,name as Subject from op_subject"""
        cursor.execute(query1)
        mycheck = [dict(line) for line in
        [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]
        print({"results": mycheck})
        return JsonResponse({"results": mycheck})

    
@api_view(["GET"])
def get_standard(request):
    if request.method == 'GET':
        cursor=connection.cursor()
        query1 = "select id,name as Standard FROM op_course ORDER BY name"
        cursor.execute(query1)
        mycheck = [dict(line) for line in
        [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]
        return JsonResponse({"results": mycheck})



@api_view(["GET","POST"])       
def get_standard_name(request):
    print("ok")
    db=json.loads(request.body)
    course_id=db['course_id']
    cursor=connection.cursor()
    query1 = "select id as course_id,name as course_name FROM op_course where id='%s'"%(course_id,)
    cursor.execute(query1)
    data = [dict(line) for line in
    [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]
    print({"results": data})
    return JsonResponse({"results": data})

@api_view(["GET"])
def get_faculty(request):
    if request.method == 'GET':
        cursor=connection.cursor()
        faculty_query = """select A.id as faculty_id,B.name as faculty_name 
        from op_faculty A join res_partner B on A.partner_id=B.id ORDER BY B.name"""
        cursor.execute(faculty_query)
        mycheck = [dict(line) for line in
        [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]
        print({"results": mycheck})
        return JsonResponse({"results": mycheck})

@api_view(["POST"])
def create_school_db(request):
    print("request bfr post check",request)
    if request.method == 'POST':
        req_data = json.loads(request.body)
        db_username = req_data['db_username']
        db_name = req_data['db_name']
        db_password = req_data['db_password']
        # contact_person_name = req_data['contact_person_name']
        app_names = 'common_custom_membership'
        # school_type = req_data['school_type']
        # school_name = req_data['school_name']
        # phone_number = req_data['phone_number']
        # master_password = req_data['master_password']
        admin_username = db_username
        admin_password = db_password
        master_password = 'admin'
        print(db_name,db_username,db_password)
        database = db_name
        server = 'http://localhost:8069'
        client = erppeek.Client(server=server)
        print(client.db.list())
        print(not database in client.db.list())
        if not database in client.db.list():
            print("The database does not exist yet, creating one!")
            client.create_database(user_password=admin_password,login=admin_username,database=database,passwd=master_password)
            data={
            "db_name": db_name,"db_username": admin_username,
            "db_password": admin_password,"app_names":app_names,
            }
            print("data are show",data)
            try:
                headers = {'Content-type': 'application/json'}
                setup_apps_list = requests.post('http://localhost:8000/setup_apps_list',headers=headers, data=json.dumps(data))
                # url='http://localhost:8000/setup_apps_list',
                # data=json.dumps(data), headers=headers)
                resp = setup_apps_list.json()
                print({"result": resp})
                return JsonResponse({'message': resp['message']})
            except Exception as e:
                print("error",e)
            # # result = resp['message']
        else:
            print("The database " + database + " already exists.")
            resp = JsonResponse({'status': 'failed', 'message': 'The database ' + database + ' already exists.'})
            resp.status_code = 500
            return resp

@api_view(["POST"])
def setup_apps_list(request):
    if request.method == 'POST':
        req_data = json.loads(request.body)
        app_names = req_data['app_names']
        db_name = req_data['db_name']
        db_username = req_data['db_username']
        db_password = req_data['db_password']
        print(db_name,db_username,db_password,app_names)
        database = db_name
        server = 'http://localhost:8069'
        db_username = db_username
        client = erppeek.Client(server, database, db_username, db_password)
        # proxy = client.model('ir.module.module')
        # installed_modules = proxy.browse([('state', '=', 'installed')])
        modules = client.modules('common_custom_membership', installed=False)
        if 'common_custom_membership' in modules['uninstalled']:
            client.install('common_custom_membership')
        else:
            print("Already installed")
            return JsonResponse({'message': 'Module is successfully installed!'})
        return JsonResponse({'message':"modules install successfully"})





