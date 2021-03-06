"""Facility Utils"""
import json
import requests

import os
import urllib3

from sef.constants import KMFL_URL, KMFL_LOGIN_URL, HEADERS

class CreateSession:
    def __init__(self):
        self.username = os.getenv('KMFL_USERNAME')
        self.password = os.getenv('KMFL_PASSWORD')
        self.session = None
        self.session_response = None

    def create_session(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        verify=True

        if not self.session and not self.session_response:
            session = requests.Session()
            self.session = session

            login_url = KMFL_URL + KMFL_LOGIN_URL
            session_response = session.post(
                url=login_url, data=json.dumps(data),headers=HEADERS,
                verify=verify)

            self.session = session
            self.session_response = session_response
