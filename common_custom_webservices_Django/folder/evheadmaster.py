def get_subject_by_standard():
    if request.method == 'GET':
        try:
            course_id = request.args['course_id']
            print(course_id)
            query1 = """Select C.id as subject_id,C.name as subject_name from op_course A
            left join op_course_op_subject_rel B on B.op_course_id=A.id
            left join op_subject C on C.id=B.op_subject_id where A.id='%s'"""%(course_id)
            cursored.execute(query1)
            mycheck = [dict(line) for line in
            [zip([column[0] for column in cursored.description], row) for row in cursored.fetchall()]]
            print({"results": mycheck})
            return jsonify({"results": mycheck})
        except Exception:
            print({"results": []})
            resp = jsonify({"results": []})
            resp.status_code = 200
            return resp