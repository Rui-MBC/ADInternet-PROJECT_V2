
import datetime
from datetime import timedelta
from flask import Flask, render_template, request, send_from_directory, jsonify, json
import os
import requests
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.operators import is_precedent
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql.sqltypes import ARRAY, DateTime
from werkzeug.utils import secure_filename
import random
app = Flask(__name__)


###########################
# GATE DATABASE ENDPOINTS #  
###########################

##vem aqui para verificar o gate, ver se o gate_id e o segredo correspondem
@app.route("/gates/id", methods = ['GET'])
def logInGate():
    ##já está, untested
    if request.method == 'GET':
        

        try:
            gateInfo = request.json 
        except:
            response = {
                    'errorCode':5,
                    'errorDescription':'DataBase had an error with JSON input.'
                }
            return jsonify(response)
        

        if not gateInfo:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        

        try:
            gateInfo["id"]
            gateInfo["secret"]
        except:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)

        
        try:
            resp = requests.get("http://localhost:8001/gates/id",json = gateInfo)
        except:
            try:
                resp = requests.get("http://localhost:8002/gates/id",json = gateInfo)
            except:
                resp = {
                    'errorCode':7,
                    'errorDescription':'counldn\'t contact any of the databases'
                }

        return jsonify(resp.json())

@app.route("/gates", methods = ['GET','PUT'])
def createGate( ):
    ##já está, untested
    if request.method == 'PUT':
    
        try:
            gateInfo = request.json 
        except:
            response = {
                    'errorCode':5,
                    'errorDescription':'DataBase had an error with JSON input.'
                }
            return jsonify(response)
    
        if not gateInfo:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'}
            return jsonify(resp)
    
        try:
            gateInfo["id"]
            gateInfo["location"]
        except:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)

        sec = random.randint(1000,9999) 

        gateInfo = {
            'id' : gateInfo["id"],
            'location' : gateInfo["location"],
            'secret':str(sec)
        } 


        #resp = gateInfo

        try:
            outcome=requests.put("http://localhost:8001/gates",json = gateInfo)
            response = outcome.json()
            if response['errorCode'] == 0:
                resp = {
                    'errorCode' : 0,
                    'errorDescription' : 'no error',
                    'secret':str(sec)
                }
              
            else:resp=response       
        except:
            resp = {
                'errorCode' : 7,
                'errorDescription' : 'Couldn´t access database.'
            }

        try:
            outcome=requests.put("http://localhost:8002/gates",json = gateInfo)
            response = outcome.json()
            if response['errorCode'] == 0: 
                resp= {
                    'errorCode' : 0,
                    'errorDescription' : 'no error',
                    'secret':str(sec)}
              
            else: resp=response       
        except:
            resp = {
                'errorCode' : 7,
                'errorDescription' : 'Couldn´t access database.'
            }

        
    

        return jsonify(resp)





@app.route("/gates/newEvent", methods = ['PUT'])
def newEvent( ):
    ##já está, untested
    if request.method == 'PUT':
        try:
            eventInfo = request.json 
        except:
            resp = {
                    'errorCode':5,
                    'errorDescription':'DataBase had an error with JSON input.'
                }
            return jsonify(resp)
        if not eventInfo:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        try:
            eventInfo["code"]
            eventInfo["gate_id"]
        except:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)

        
        try:
            resp = requests.put("http://localhost:8001/gates/newEvent",json = eventInfo)
        except:
            resp = {
                'errorCode' : 7,
                'errorDescription' : 'Couldn´t access database.'  
            }

        try:
            resp = requests.put("http://localhost:8002/gates/newEvent",json = eventInfo)
        except:
            resp = {
                'errorCode' : 7,
                'errorDescription' : 'Couldn´t access database.'  
            }
            return jsonify(resp)


        return jsonify(resp.json())



@app.route("/gates/activity", methods = ['GET'])
def gatesActivity( ):


    try:
        resp = requests.get("http://localhost:8001/gates/activity" )
    except:
        resp = {
            'errorCode' : 7,
            'errorDescription' : 'Couldn´t access database.'
        } 
    try:
        resp = requests.get("http://localhost:8002/gates/activity" )
    except:
        resp = {
            'errorCode' : 7,
            'errorDescription' : 'Couldn´t access database.'
        } 
 

    return resp.json()




    
if __name__ == "__main__":
    app.run(host = 'localhost', port = 8000, debug = True)    