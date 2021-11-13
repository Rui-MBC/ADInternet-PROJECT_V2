
import datetime
from datetime import timedelta
from flask import Flask, render_template, request, send_from_directory, jsonify, json
import os
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.operators import is_precedent
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql.sqltypes import ARRAY, DateTime
from werkzeug.utils import secure_filename
import userData as uD
from userData import session
import random
app = Flask(__name__)


###########################
# GATE DATABASE ENDPOINTS #
###########################
@app.route("/users/user", methods = ['PUT'])
def newUser():
    if request.method == 'PUT':
        try:
            userInfo = request.json 
        except:
            response = {
                    'errorCode':5,
                    'errorDescription':'DataBase had an error with JSON input.'
                }
            return jsonify(response)
        if not userInfo:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        try:
            userInfo["id"]
            userInfo['secret']
        except:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        if not uD.getUserById(userInfo["id"]):  
            uD.newUser(userInfo["id"],'',userInfo['secret'],datetime.datetime.now())
        else:
            uD.setNewUserSecret(userInfo["id"],userInfo['secret']) 
        
        resp = {
                'errorCode' : 0,
                'errorDescription':''
            }
        return jsonify(resp)

@app.route("/users/validUser", methods = ['GET'])
def validateUser():
    if request.method == 'GET':
        try:
            userInfo = request.json 
        except:
            response = {
                    'errorCode':5,
                    'errorDescription':'DataBase had an error with JSON input.'
                }
            return jsonify(response)
        if not userInfo:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        try:
            userInfo["id"]
        except:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        User=uD.getUserById(userInfo["id"])
        user =User.as_json()
        resp = {
                'errorCode' : 0,
                'errorDescription':'',
                'userId':user['id'],
                'userSecret':user['secret'],
        }
        return jsonify(resp)

@app.route("/users/qrcode", methods = ['PUT'])
def logInUser():
    if request.method == 'PUT':
        try:
            userInfo = request.json 
        except:
            response = {
                    'errorCode':5,
                    'errorDescription':'DataBase had an error with JSON input.'
                }
            return jsonify(response)
        if not userInfo:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        try:
            userInfo["id"]
            userInfo["code"]
        except:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)   
        uD.setNewUserCode(userInfo["id"],userInfo["code"],datetime.datetime.now()) 
        resp = {
                'errorCode' : 0,
                'errorDescription':''
            }
        return jsonify(resp)

@app.route("/users/history", methods = ['GET'])
def history():
    info = request.json 
    user = info["user"]
    user_list = uD.history_list(user)
    print(user_list)
    return {"list" : user_list}


@app.route("/users/code", methods = ['GET'])
def verifycode():
    if request.method == 'GET':
        try:
            userInfo = request.json 
        except:
            response = {
                    'errorCode':5,
                    'errorDescription':'DataBase had an error with JSON input.'
                }
            return jsonify(response)
        if not userInfo:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        try:
            userInfo["id"]
            userInfo["code"]
            userInfo["gate_id"]
        except:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)
        resp=uD.validateCode(userInfo["id"],userInfo["code"])
        #print(resp)
        if resp["errorCode"]==0:
            uD.newOpenGate(userInfo["id"],userInfo["gate_id"],datetime.datetime.now())
        
        return resp




if __name__ == "__main__":
    app.run(host = 'localhost', port = 6000, debug = True)    