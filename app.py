
''' == Imports == '''
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for;
import json;
import requests;
import base64
import pyrebase

''' == Global variables == '''
app = Flask(__name__)
firebaseConfig = {
    "apiKey": "AIzaSyAY2ai-xYdAassFY4bSQg-IGjayiDIPKD4",
    "authDomain": "beemathon.firebaseapp.com",
    "databaseURL": "https://beemathon-default-rtdb.firebaseio.com",
    "projectId": "beemathon",
    "storageBucket": "beemathon.appspot.com",
    "messagingSenderId": "588525140503",
    "appId": "1:588525140503:web:ad1442d1140835a102ba52",
    "measurementId": "G-2FCBG4EM97"
    };
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
database = firebase.database()
uid = ""
category = ""

''' == Pages == '''

# Signup
@app.route("/", methods=["POST", "GET"])
def signup():
    if (request.method == "POST"):
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone_number = request.form["phoneNumber"]
        global category
        category = request.form["category"]
        user = auth.create_user_with_email_and_password(email, password)
        global uid
        uid = user['localId']
        database.child(category).child("buisnesses").child(uid).update({
            "name": name,
            "phoneNumber": phone_number
        })
        return redirect(url_for("community"))
    else:
        return render_template('signup.html')

# Home
@app.route("/home")
def home():
    return redirect(url_for("community"))

# Community
@app.route("/home/community")
def community():
        return render_template('home.html')

# SMS
@app.route("/home/community/send", methods=['GET','POST'])
def send():
    if (request.method == "POST"):
        message = request.form["message"]
        recipients =  [
            {
                'recipient_id': 1,
                'dest_addr': '255692189307',
            },
        ]
        name = database.child("buisnesses").child(uid).child("name").get().val()
        return redirect(url_for("send_sms", name=name, message=message,recipients=recipients))
    else:
        return redirect(url_for("community"))

# SMS Request
@app.route("/home/community/send/<name>/<message>/<recipients>")
def send_sms(name, message, recipients):

    formatted_message = "message from " + name + ": " + message
    URL = 'https://apisms.beem.africa/v1/send'
    api_key = 'b5eb8d4327dfedaf'
    secret_key = 'ZWU5YmJmZDJmYjEzZjI3NDkwN2YwYWMxMjYxN2E0OTFkZWQwZDdlZWQ0YWNmZWEwYjYyMDJlZjgwYzdlNjA2Yg=='
    content_type = 'application/json'
    source_addr = 'INFO'
    apikey_and_apisecret = api_key + ':' + secret_key

    first_request = requests.post(url = URL,data = json.dumps({
        'source_addr': source_addr,
        'schedule_time': '',
        'encoding': '0',
        'message': formatted_message,
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

    return redirect(url_for("community"))

# USSD callback
@app.route('/home/share/ussd/callback',methods=['GET','POST'])
def USSDCallback():
    if request.method == 'POST':
        '''
        data = {
            "command": "initiate",
            "msisdn": "255692189307",
            "session_id": "689970",
            "operator": "tigotz",
            "payload": {
                "request_id": 1,
                "response": 0,
            }
        }
        '''
        data = request.get_json()
        if data:
            print(data)
            msisdn1=data['msisdn']
            operator1= 'tigo'#data['operator']
            session_id1=data['session_id']
            myresponse=data['payload']['response']
            payload_data={}
            request_id = 0
            if data['payload']['request_id']:
                request_id = int(data['payload']['request_id'])

            ussd_menu = [{"text": "1. Join Jamii Moja" }, { "text" : "Enter phone number" }, { "text": "Enter name" }]
            #request_message = ussd_menu[request_id]['text']
            command = "terminate" if request_id + 1 == len(ussd_menu) else "continue"

            payload_data = {
                'request_id': '0',
                'request': str(request_id)
            }

            newData = {
                'msisdn':msisdn1,
                'operator':operator1,
                'session_id':session_id1,
                'command': 'continue',
                'payload':payload_data
            }

            return Response (
                json.dumps(newData),
                status=200,
            )
    else:
        newData = {
         'msisdn':'255762265939',
         'Operator':'vodacom',
         'session_id':'14545',
         'command':'initiate',
         'payload':{
             'request_id':'0',
             'response':'enter phone number'
            }
        }

        return Response(
             json.dumps(newData),
             status=200,
        )

@app.errorhandler(500)
def server_error(e):
    errorName='Error'
    return Response(
        json.dumps(errorName),
        status=500,
    )

if __name__ == '__main__':
    app.run(debug=True)
