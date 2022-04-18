# File containing every functions that are necessary to get the access token

from flask import Flask, request
import flask
import time
import requests

import data
from data import membership_types, membership_ids, characters_ids


my_api_key = data.my_api_key


# class containing every data bungie application needs to work
class Application:
    """
    Attributes:
    :param client_id:
        the ClientId of the application
    :param client_secret:
        the ClientSecret of the application
    :param api_key:
        the API key of the application
    :param port:
        the port of the server
    :param host:
        the host of the server
    :param redirect_url:
        the redirect url of the application
    """

    client_id = ''
    port = ''
    client_secret = ''
    api_key = ''
    host = ''
    redirect_url = ''
    code_found = 0
    token = {}
    authorization_code = ''
    membership_types = membership_types
    membership_ids = membership_ids
    character_ids = characters_ids

    def __init__(self, client_id, client_secret, host, port, api_key, redirect_url=''):
        self.client_id = str(client_id)
        self.client_secret = client_secret
        self.host = host
        self.port = str(port)
        self.redirect_url = redirect_url
        self.api_key = api_key


me = Application(39929, 'TMoN2NYNXc10FtI5OuIc0DnL6v7NewvqFHJxJ6bt21Q', '0.0.0.0', 5000, my_api_key)

app = Flask(__name__)


@app.route('/')
def authorize():
    authorize_url = 'https://www.bungie.net/en/oauth/authorize?client_id=' + str(me.client_id) + '&response_type=code' \
                                                                                                 '&state=asdf '
    if me.code_found == 0:
        me.code_found = 1
        return flask.redirect(authorize_url)
    else:
        if 'code' in request.args:
            me.authorization_code = request.args['code']
        else:
            return flask.redirect('/shutdown')
        return flask.redirect('/redirect_url')


# shutdown the current server
@app.route('/end')
def end():
    return 'OK'


# get the redirect url from the "me" application with the authorization code got above
@app.route('/redirect_url')
def redirect():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data_ = {
        'grant_type': 'authorization_code',
        'client_id': me.client_id,
        'client_secret': me.client_secret,
        'code': me.authorization_code
    }
    print("before")

    r = requests.post('https://www.bungie.net/platform/app/oauth/token/', data=data_, headers=headers)
    resp = r.json()
    print(resp)
    data.auth_token = resp['access_token']

    me.token = {
        'access_token': resp['access_token'],
        'refresh': resp['refresh_token'],
        'expires': time.time() + resp['refresh_expires_in']
    }
    print("access token saved")
    return flask.redirect('/end')
