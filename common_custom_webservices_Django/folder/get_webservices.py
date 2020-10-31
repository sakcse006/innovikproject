from flask import Flask, request,send_file
exp_time = ""
app = Flask(__name__)

#from flask_restful import Resource, Api
#from flask_cors import CORS, cross_origin

#api = Api(app)
#RS(app)



#@app.route('/get_test_webservices_function', methods=['GET','POST'])
def get_test_webservices_function():
    print('inside webservices method')

if _name_ == "__main__":
    print("am going to start the server using run method")
    app.run(host='0.0.0.0',port='5001')
    get_test_webservices_function()Type a message