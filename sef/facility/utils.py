"""Case Utils"""
import os


def create_session():
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    data = {
        'username': username,
        'password': password
    }
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    verify=True

    session = requests.Session()

    session_response = session.post(
        url=loginURL, data=json.dumps(data), headers=headers, verify=verify)

    return (s, session_response)
