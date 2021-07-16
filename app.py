
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

''' == Pages == '''
@app.route("/", methods=["POST", "GET"])
def signup():
    if (request.method == "POST"):
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        phone_number = request.form["phoneNumber"]
        user = auth.create_user_with_email_and_password(email, password)
        global uid
        uid = user['idToken'][:11]
        database.child("users").child(uid).update({
            "name": name,
            "phoneNumber": phone_number
        })
        return redirect(url_for("community"))
    else:
        return render_template('signup.html')

@app.route("/home")
def home():
    return redirect(url_for("community"))

@app.route("/home/community")
def community():
        return render_template('home.html')

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
        name = database.child("users").child(uid).child("name").get().val()
        return redirect(url_for("send_sms", name=name, message=message,recipients=recipients))
    else:
        return redirect(url_for("community"))

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

@app.errorhandler(500)
def server_error(e):
    errorName='Error'
    return Response(
        json.dumps(errorName),
        status=500,
    )

if __name__ == '__main__':
    app.run(debug=True)
