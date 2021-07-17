
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
        try:
            user = auth.create_user_with_email_and_password(email, password)
            global uid
            uid = user['localId']
            database.child("businesses").child(category).child(uid).update({
                "name": name,
                "phoneNumber": phone_number
            })
            return redirect(url_for("community"))
        except:
            return redirect(url_for("signup", error_message="Change username or password"))
    else:
        error_message = request.args.get("error_message")
        if (error_message == None):
            error_message = ""
        return render_template('signup.html', error_message=error_message)

# Home
@app.route("/home")
def home():
    return redirect(url_for("community"))

# Community
@app.route("/home/community")
def community():
        error_message = request.args.get("error_message")
        if (error_message == None):
            error_message = ""
        return render_template('home.html', error_message=error_message)

# SMS
@app.route("/home/community/send", methods=['GET','POST'])
def send():
    if (request.method == "POST"):
        message = request.form["message"]
        recipients = []
        stored_recipients = database.child("recipients").get().val()
        if stored_recipients:
            for subscriber_id, phone_number in stored_recipients.items():
                recipients.append({"request_id": subscriber_id, "request": phone_number})
        try:
            name = database.child("businesses").child(category).child(uid).child("name").get().val()
            if len(recipients) > 0:
                print("yes")
                return redirect(url_for("send_sms", name=name, message=message,recipients=recipients))
            else:
                return redirect(url_for("community", error_message="No members in your community"))
        except Exception as e:
            return f"<h1> {e} </h1>"
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
        'recipients': recipients,
    }),

    headers = {
        'Content-Type': content_type,
        'Authorization': 'Basic ' + api_key + ':' + secret_key,
         },
    auth=(api_key,secret_key),verify=False)

    return redirect(url_for("community"))

# Info
@app.route('/home/info')
def info():
    name = database.child("businesses").child(category).child(uid).child("name").get().val()
    number = database.child("businesses").child(category).child(uid).child("phoneNumber").get().val()
    return render_template('info.html', name=name, number=number, category=category, ussd='123# (hardcoded)')

# Feedback 
@app.route('/home/feedback')
def feedback():
    return render_template('feedback.html')

# USSD callback
@app.route('/home/share/ussd/callback',methods=['GET','POST'])
def USSDCallback():
    if request.method == 'POST':
        data = request.get_json()
        if data:
            print(data)
            msisdn1=data['msisdn']
            operator1= 'tigo'#data['operator']
            session_id1=data['session_id']
            phone_number=data['payload']['response']
            payload_data={}
            request_id = 0
            if data['payload']['request_id']:
                request_id = int(data['payload']['request_id'])

            ussd_menu = [{"text": "1. Join Jamii Moja" }, { "text" : "Enter phone number" }, { "text": "Enter name" }]
            #request_message = ussd_menu[request_id]['text']
            command = "terminate" if request_id + 1 == len(ussd_menu) else "continue"

            if (phone_number != 0):
                database.child("recipients").push(phone_number)

            payload_data = {
                'request_id': request_id + 1,
                'request': ussd_menu[1]["text"]
            }

            newData = {
                'msisdn':msisdn1,
                'operator':operator1,
                'session_id':session_id1,
                'command': "terminate",
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
