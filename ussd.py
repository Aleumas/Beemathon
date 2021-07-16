from flask import Flask,request,jsonify,Response;
import json;
import requests;
#import pyodbc;

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def USSDCallback():
    if request.method == 'POST':
        data = request.get_json()
        if data:
            print(data)
            print(data['payload']['response'])
            msisdn1=data['msisdn']
            operator1= 'tigo'#data['operator']
            session_id1=data['session_id']
            command1= 'command'#data['command']
            myresponse=data['payload']['response']
            payload_data={}

            if myresponse == '99':
                payload_data={
                    'request_id':'0',
                    'request':'1. enter first phone number'
                }
                command1 = 'continue-1*1'

                newData = {
                    'msisdn':msisdn1,
                    #'operator':operator1,
                    'session_id':session_id1,
                    'command':command1,
                    'payload':payload_data
                }

                return Response(
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
