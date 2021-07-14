from flask import Flask,request,jsonify,Response;
import json;
import requests;
import base64
#import pyodbc;
app = Flask(__name__)

@app.route('/home',methods=['GET','POST'])
def send_sms():

    URL = 'https://apisms.beem.africa/v1/send'
    api_key = 'b5eb8d4327dfedaf'
    secret_key = 'ZWU5YmJmZDJmYjEzZjI3NDkwN2YwYWMxMjYxN2E0OTFkZWQwZDdlZWQ0YWNmZWEwYjYyMDJlZjgwYzdlNjA2Yg=='
    content_type = 'application/json'
    source_addr = '255692189307'
    apikey_and_apisecret = api_key + ':' + secret_key

    first_request = requests.post(url = URL,data = json.dumps({
        'source_addr': source_addr,
        'schedule_time': '',
        'encoding': '0',
        'message': 'SMS Test from Python API.',
        'recipients': [
            {
                'recipient_id': 1,
                'dest_addr': '255692189307',
            },
        ],
    }),

    headers = {
        'Content-Type': content_type,
        'Authorization': 'Basic ' + api_key + ':' + secret_key,
         },
    auth=(api_key,secret_key),verify=False)

    print("== Request ==")
    print(first_request)
    print("== Other ==")
    print(first_request.status_code)
    print(first_request.json())
    return (first_request.json())

@app.errorhandler(500)
def server_error(e):
    errorName='Error'
    return Response(
        json.dumps(errorName),
        status=500,
    )

if __name__ == '__main__':
    app.run(debug=True)
