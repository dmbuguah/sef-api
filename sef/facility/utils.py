"""Facility Utils"""
import json
import requests

import os
import urllib3

from sef.constants import KMFL_URL, KMFL_LOGIN_URL, HEADERS

def create_session():
    username = os.getenv('KMFL_USERNAME')
    password = os.getenv('KMFL_PASSWORD')

    data = {
        'username': username,
        'password': password
    }
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    verify=True

    session = requests.Session()

    login_url = KMFL_URL + KMFL_LOGIN_URL
    import pdb; pdb.set_trace()
    session_response = session.post(
        url=login_url, data=json.dumps(data), headers=HEADERS, verify=verify)

    return (session, session_response)
