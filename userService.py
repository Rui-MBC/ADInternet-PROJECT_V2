
import datetime
from datetime import timedelta
from flask import Flask, render_template, request, send_from_directory, jsonify, json
import os
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


@app.route("/users/id", methods = ['PUT'])
def logInGate():
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
            userInfo["secret"]
        except:
            resp = {
                'errorCode' : 5,
                'errorDescription':'database had an error with JSON input.'
            }
            return jsonify(resp)    





if __name__ == "__main__":
    app.run(host = 'localhost', port = 6000, debug = True)    