
import datetime
from datetime import timedelta
from flask import Flask, render_template, request, send_from_directory, jsonify, json
import os
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.operators import is_precedent
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql.sqltypes import ARRAY, DateTime
from werkzeug.utils import secure_filename
import gateData1 as gD
from gateData1 import session
import random
app = Flask(__name__)


###########################
# GATE DATABASE ENDPOINTS #  
###########################








##vem aqui para verificar o gate, ver se o gate_id e o segredo correspondem
@app.route("/gates/id", methods = ['GET'])
def logInGate():
    
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
                'errorDescription':'database had an error with JSON input.'}
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


        gate = gD.getGateById(gateInfo["id"])
        
        if gate != None :
            if gate.secret == gateInfo["secret"]:
                response = {
                    'errorCode':0,
                    'errorDescription':'no error'}
            else:
                response = {
                    'errorCode':1,
                    'errorDescription':'The secret is not valid for this gate.'}
            
        else:
            response = {
                    'errorCode':3,
                    'errorDescription':'No gate found for this ID.'
                    }

        return jsonify(response)




@app.route("/gates", methods = ['GET','PUT'])
def createGate( ):
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
                'errorDescription':'database had an error with JSON input.'
            }
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

        
        if not gD.getGateById(int(gateInfo["id"])):
            gD.newGate(int(gateInfo["id"]), gateInfo["secret"] ,gateInfo["location"])
            response = {
                    'errorCode':0,
                    'errorDescription':'no error'
                }        
        else:
            response = {
                    'errorCode':4,
                    'errorDescription':'Gate id not available.'
                }
        return jsonify(response)
        #return str(sec)
    if request.method == 'GET':
        return jsonify(gD.listGate())



@app.route("/gates/newEvent", methods = ['PUT'])
def newEvent( ):
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

        gD.newEvent(int(eventInfo["gate_id"]),eventInfo["code"],datetime.datetime.now())
        resp = {
                'errorCode' : 0,
                'errorDescription':'no error'
            }
        return jsonify(resp)

@app.route("/gates/activity", methods = ['GET'])
def gatesActivity( ):
    try:
        gates_list = gD.Activity_list()
        return {"list" : gates_list}
    except:
        return {"list" : []}

if __name__ == "__main__":
    app.run(host = 'localhost', port = 8001, debug = True)    