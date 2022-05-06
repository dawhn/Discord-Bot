# File containing every functions that are necessary to get the access token

# imports
import flask
import time
import requests
import pandas as pd

# from imports
from flask import Flask, request

# file imports
import data

# from file imports
from data import membership_types, membership_ids, characters_ids

my_api_key = data.my_api_key
app = Flask(__name__)


# classes containing every data bungie application needs to work
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


def get_stored_informations():
    """
    Check for wether data about the access_token is stored locall or not
    - Yes: Parse it to the object me of the classes Application
    - No: Do nothing
    :return: return wether ../data.csv exists
    """
    try:
        data_ = pd.read_csv(r'../data.csv')
    except FileNotFoundError as e:
        print(e)
        return False
    df = pd.DataFrame(data_)
    df = df.iloc[0]
    me.token['access_token'] = df['access_token']
    me.token['access_expires'] = df['access_expires']
    me.token['refresh_token'] = df['refresh_token']
    me.token['refresh_expires'] = df['refresh_expires']
    return True


@app.route('/')
def authorize():
    """
    Get the authorization code by authorizing the application with a valid bungi.net account
    :return: redirect the server to /redirect_url if all went wall, /end otherwise
    """

    authorize_url = 'https://www.bungie.net/en/oauth/authorize?client_id=' + str(me.client_id) + '&response_type=code' \
                                                                                                 '&state=asdf '
    if me.code_found == 0:
        me.code_found = 1
        return flask.redirect(authorize_url)
    else:
        if 'code' in request.args:
            me.authorization_code = request.args['code']
        else:
            return flask.redirect('/end')
        return flask.redirect('/redirect_url')


@app.route('/end')
def end():
    """
    Simple return to avoid shutdowning the server but doesn't do anything more
    :return:
    """

    return 'OK'


@app.route('/redirect_url')
def redirect():
    """
    Get the access_token, the refresh_token with their respective expiration date and store them in "me"
    :return: redirect the server to /end
    """

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data_ = {
        'grant_type': 'authorization_code',
        'client_id': me.client_id,
        'client_secret': me.client_secret,
        'code': me.authorization_code
    }

    r = requests.post('https://www.bungie.net/platform/app/oauth/token/', data=data_, headers=headers)
    resp = r.json()
    data.auth_token = resp['access_token']

    me.token = {
        'access_token': resp['access_token'],
        'access_expires': time.time() + resp['expires_in'],
        'refresh_token': resp['refresh_token'],
        'refresh_expires': time.time() + resp['refresh_expires_in']
    }
    print("access token saved")
    return flask.redirect('/end')


@app.route('/refresh_url')
def refresh():
    """
    Refresh the access_token, the new refresh_token with their respective expiraiton date and store them in "me"
    :return: redirect the server to /end
    """

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data_ = {
        'grant_type': 'refresh_token',
        'refresh_token': me.token['refresh_token'],
        'client_id': me.client_id,
        'client_secret': me.client_secret
    }

    r = requests.post('https://www.bungie.net/platform/app/oauth/token/', data=data_, headers=headers)
    resp = r.json()

    me.token['access_token'] = resp['access_token']
    me.token['access_expires'] = time.time() + resp['expires_in']
    me.token['refresh_token'] = resp['refresh_token']
    me.token['refresh_expires'] = time.time() + resp['refresh_expires_in']

    # Replace csv file with new data
    data_ = {'access_token': [me.token['access_token']],
             'access_expires': [me.token['access_expires']],
             'refresh_token': [me.token['refresh_token']],
             'refresh_expires': [me.token['refresh_expires']]}
    df = pd.DataFrame(data_)
    df.to_csv('../data.csv')

    print("refresh token used and access token saved")
    return flask.redirect('/end')
