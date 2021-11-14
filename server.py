from logging import raiseExceptions
from requests_oauthlib import OAuth2Session
from flask import Flask, render_template,request, redirect, session, url_for
from flask.json import jsonify
import qrcode 
import random
import string
import os
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import requests
import time
from flask import make_response


app = Flask(__name__)


# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
client_id = "851490151334137"
client_secret = "J05ujBUfQVqy0Y6ElVBW6j9QtkzaZpz5uWeWIY/45n5XgWKLXwtxj/sBvIjXKz9C0ikKwj1Iwq8LON9UuGXALA=="
authorization_base_url = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog'
token_url = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

@app.route("/", methods=["GET"])
def home():  
   
    return render_template('home.html')


@app.route("/login/<path:type>")
def login(type):
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    github = OAuth2Session(client_id, redirect_uri="http://localhost:5000/callback")
    authorization_url, state = github.authorization_url(authorization_base_url)
    #print( authorization_url)
    #print(state)
    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    session['type'] = type
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    print("CALLABACK")

    print(request.url)
    github = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri="http://localhost:5000/callback")
    #print(github.authorized)
    print("a")
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    #session['oauth_token'] = token
    github = OAuth2Session(client_id, token=token)
    info = github.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person').json()
    #print(info ,"\n\n\n")
    #session.pop("oauth_state")
    session['username'] = info['username']
    session["secret"] =str(os.urandom(24))
    #print(str(session['oauth_token']['access_token']))
    user_info={
        'id' : session['username'],
        'secret' : str(session['secret'])
    }
    try:
        resp = requests.put("http://localhost:6000/users/user",json = user_info)
    except:
        resp = {
            'errorCode' : 7,
            'errorDescription' : 'Couldn´t access database.'
        } 
     #meter username e token na bd
    url = "."+session['type']

    return redirect(url_for(url))
    
@app.route("/adminapp", methods=["GET"])
def adminapp(): 
    try:        

        user = session["username"]
        secret = session["secret"]
        if"adminapp" == session['type'] :
            print("\n type is right   : ", session['type'])
        else:raise ValueError("")
        userdata = {
            'id' : user
        }
        
        try:
            resp = requests.get("http://localhost:6000/users/validUser",json = userdata)
        except:
            return redirect(url_for(".home"))

        userInfo = resp.json()
        if (userInfo['errorCode']==0):
            if(userInfo['userId']==user and userInfo['userSecret']==secret):
                pass
            else:raiseExceptions
        else:raiseExceptions
    except :
        return redirect(url_for(".login",type="adminapp")) 
    return render_template('admin.html')



@app.route("/adminapp/activity", methods=['GET'])
def returnsActivity():
    try:
        resp = requests.get("http://localhost:8000/gates/activity" )
    except:
        resp = {
            'errorCode' : 7,
            'errorDescription' : 'Couldn´t access database.'
        } 
        return jsonify(resp) 
    return resp.json()

@app.route("/adminapp/gate",methods = ['GET','POST'])
def createGate():  
    if request.method == 'POST':   
        try:
            form_content = request.get_json()
            id= int(form_content['id'])
        except:
            resp = {
                'errorCode' : 9,
                'errorDescription' : '!!! Bad form !!!'
            }
            return jsonify(resp)

        if not form_content or not form_content['id'] or not form_content["location"]:
            
            resp = {
                'errorCode' : 9,
                'errorDescription' : '!!! Bad form !!!'
            }
            return jsonify(resp)

        create_gate_cont = {
            'id':form_content['id'],
            'location':form_content["location"]
        }
        try:
            resp = requests.put("http://localhost:8000/gates",json = create_gate_cont)
        except:
            resp = {
                'errorCode' : 7,
                'errorDescription' : 'Couldn´t access database.'
            }
            return jsonify(resp)
        return jsonify(resp.json())


@app.route("/userapp", methods=["GET"])
def userapp(): 
    try:
        user = session["username"]
        secret = session["secret"]

        if"userapp" == session['type'] :
            print("type is right   : ", session['type'])
        else:raise ValueError("")        
        print (user, secret,type)
        userdata = {
            'id' : user
        }

        try:
            resp = requests.get("http://localhost:6000/users/validUser",json = userdata)
        except:
            return redirect(url_for(".home"))

        userInfo = resp.json()
        if (userInfo['errorCode']==0):
            if(userInfo['userId']==user and userInfo['userSecret']==secret):
                pass
            else:raiseExceptions
        else:raiseExceptions
    except:
        return redirect(url_for(".login",type="userapp"))

    return render_template('user.html')

@app.route("/gateapp", methods=["GET"])
def gateapp():   
    return render_template('qr_read.html')


@app.route("/API/gateapp/code", methods=["POST"])
def gatecode(): 
    if request.method=='POST':
        try:
            userinfo = request.get_json()
            userinfo[0]["id"]
            userinfo[0]["code"]
            userinfo[1]["gate_id"]
        except:
            resp = {
                'errorCode' : 9,
                'errorDescription' : '!!! Bad form !!!'
            }
            return jsonify(resp)

        userdata = {
            'id' : userinfo[0]["id"],
            'code' : userinfo[0]["code"],
            "gate_id" :userinfo[1]["gate_id"]
        }
    

    try:
        resp = requests.get("http://localhost:6000/users/code",json = userdata)
    except:
        resp = {
            'errorCode' : 7,
            'errorDescription' : 'Couldn´t access database.'  
        }
        return jsonify(resp)

    resp = resp.json()
    if(resp['errorCode'] == 0):
        validation = "Success"
    else:
        validation = "Fail to Open"

    eventData={
            'code' : validation,
            "gate_id" :userinfo[1]["gate_id"]
        }

    try:
        requests.put("http://localhost:8000/gates/newEvent",json = eventData)
    except:
        resp = {
            'errorCode' : 7,
            'errorDescription' : 'Couldn´t access database.'  
        }
    
    return jsonify(resp)
        

@app.route("/gateapp/gate", methods=["POST"])
def gate(): 
        
        try:
            form_content = request.get_json()
            id= int(form_content['id'])
        except:
            resp = {
                'errorCode' : 9,
                'errorDescription' : '!!! Bad form !!!'
            }
            return jsonify(resp)

        if not form_content or not form_content['id'] or not form_content['secret']:
            
            resp = {
                'errorCode' : 9,
                'errorDescription' : '!!! Bad form !!!'
            }
            return jsonify(resp)

        verify_gate = {
            'id':form_content['id'],
            'secret':form_content["secret"]
        }

        try:
            resp = requests.get("http://localhost:8000/gates/id",json = verify_gate)
        except:
            resp = {
                'errorCode' : 7,
                'errorDescription' : 'Couldn´t access database.'
                 
            }
            return jsonify(resp)  

        return jsonify(resp.json())









@app.route("/API/users/code", methods=["GET"])
def code_gen(): 
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
    user_info={
        'id' : session['username'],
        'code' : code
    }
    try:
        resp = requests.put("http://localhost:6000/users/qrcode",json = user_info)
        response = resp.json()
    except:
        resp = {
            'errorCode' : 7,
            'errorDescription' : 'Couldn´t access database.'
        } 
    if response['errorCode'] == 0:
        return jsonify(user_info)
    else:
        return response

@app.route("/userapp/history", methods=["GET"])
def history(): 
    info = {"user" : session["username"]}
    try:
        resp = requests.get("http://localhost:6000/users/history",json =info)
        response = resp.json()
    except:
        resp = {
            'errorCode' : 7,
            'errorDescription' : 'Couldn´t access database.'
        } 
    

    return response  




if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(24)
    app.run(host = 'localhost', port = 5000, debug = True)