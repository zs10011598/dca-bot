import os
import time
import hmac
import hashlib
import requests
import json
import helpers



def do_bitso_request(url, request_path, http_method, parameters):
    '''
        Description: creates signing request for bitso API
    '''
    bitso_key = os.environ['API_KEY']
    bitso_secret = os.environ['API_SECRET']

    nonce = str(int(round(time.time() * 1000)))
    message = nonce+http_method+request_path

    if http_method == 'POST':
        message += json.dumps(parameters)

    signature = hmac.new(bitso_secret.encode('utf-8'), 
                        message.encode('utf-8'),
                        hashlib.sha256).hexdigest()

    auth_header = 'Bitso %s:%s:%s' % (bitso_key, nonce, signature)
    headers = {'Authorization': auth_header}

    if http_method == 'GET':
        res = requests.get(url, headers=headers)
    elif http_method == 'POST':
        res = requests.post(url, json=parameters, headers=headers)

    return res.json()


def get_bitso_balance():
    '''
        Description: get balance in bitso account
    '''
    routes = helpers.get_routes('bitso')
    url = routes['get_balance']
    request_path = routes['get_balance_path']
    http_method = 'GET'
    parameters = {}
    res = do_bitso_request(url, request_path, http_method, parameters)
    return float(res['payload']['balances'][0]['available'])