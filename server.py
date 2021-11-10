from requests_oauthlib import OAuth2Session
from flask import Flask, render_template,request, redirect, session, url_for
from flask.json import jsonify
import qrcode 
import random
import string
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import requests


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


@app.route("/<path:type>")
def demo(type):
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    github = OAuth2Session(client_id, redirect_uri="http://localhost:5000/callback")
    authorization_url, state = github.authorization_url(authorization_base_url)
    print(authorization_url)
    print(state)
    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    session['messages'] = type
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
    print(github.authorized)
    print("a")
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token
    github = OAuth2Session(client_id, token=session['oauth_token'])
    info = github.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person').json()
    print(info)
    session['username'] = info['username']
    user_info={
        'id' : session['username']
    }
    try:
        resp = requests.put("http://localhost:6000/users/user",json = user_info)
    except:
        resp = {
            'errorCode' : 7,
            'errorDescription' : 'Couldn´t access database.'
        } 
     #meter username e token na bd
    url = "."+session['messages']+"app"

    return redirect(url_for(url))
    
@app.route("/adminapp", methods=["GET"])
def adminapp():   
    return render_template('newGate.html')

@app.route("/adminapp/createGate",methods = ['GET','POST'])
def createGate():  
    if request.method == 'POST':
        form_content = request.form.to_dict()
        try:
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
        print(resp.json())
        return jsonify(resp.json())


@app.route("/userapp", methods=["GET"])
def userapp():   
    return render_template('layout.html')

@app.route("/gateapp", methods=["GET"])
def gateapp():   
    return render_template('gate.html')

@app.route("/gateapp/gate", methods=["POST"])
def gate(): 

        form_content = request.form.to_dict()
        try:
            id= int(form_content['id'])
        except:
            resp = {
                'errorCode' : 92,
                'errorDescription' : '!!! Bad form !!!'
            }
            return jsonify(resp)

        if not form_content or not form_content['id'] or not form_content['secret']:
            
            resp = {
                'errorCode' : 91,
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
            return jsonify(resp.json())     
        return render_template('qr_read.html')

@app.route("/API/users/code", methods=["GET"])
def code_gen(): 
    code = session['username'] + ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
    user_info={
        'id' : session['username'],
        'code' : code
    }
    try:
        resp = requests.put("http://localhost:6000/users/qrcode",json = user_info)
    except:
        resp = {
            'errorCode' : 7,
            'errorDescription' : 'Couldn´t access database.'
        } 
    response = resp.json()
    if response['errorCode'] == 0:
        return {'code': code}
    else:
        return response

@app.route("/userapp/history", methods=["GET"])
def history():   
    return app.send_static_file('layout.html')



if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.secret_key = os.urandom(24)
    app.run(host = 'localhost', port = 5000, debug = True)