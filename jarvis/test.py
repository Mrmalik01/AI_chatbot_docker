import requests
from cred import USER_KEY, WATSON_KEY
import json

#response = requests.get('http://%7B{}%7D/%7Bmethod%7D'.format(WATSON_KEY['url']), auth=('apikey', '{}'.format(WATSON_KEY['key'])))
#print(response)

id = ""
def retrieve_access_token():
        url = USER_KEY['auth_url']
        headers = {"Content-Type" : "application/x-www-form-urlencoded", "Accept": "application/json"}
        data = {"apikey" : WATSON_KEY['key'], "grant_type" : "urn:ibm:params:oauth:grant-type:apikey"}
        response = requests.post(url, data, headers= headers)
        print(response)
        if response.status_code == 200 or response.status_code == 201:
            print("Access_token retrieved")
            response = json.loads(response.text)
            id = response['access_token']
            USER_KEY['access_token'] = response['access_token']
            USER_KEY['refresh_token'] = response['refresh_token']
            return True
        print("Access-token extraction failed")

def _create_session():
        params = (
            ('version', '2019-02-28'),
        )
        response = requests.post(
            '{}/v2/assistants/{}/sessions'.format(WATSON_KEY['url'], 
            WATSON_KEY['assistant_id']), 
            params=params, 
            auth=('apikey', WATSON_KEY['key']))
        response = json.loads(response.text)
        session_id = response.get("session_id")
        if session_id :
            USER_KEY["session_id"] = session_id
            print("Session with IBM Watson created")
            return True
        print("Session problem")
        return False

def _delete_session():
        params = (
            ('version', '2019-02-28'),
        )
        response = requests.delete(
            '{}/v2/assistants/{}/sessions/8d654389-798f-4f4a-a64f-25f20c54996e'.format(WATSON_KEY['url'], 
            WATSON_KEY['assistant_id']), 
            params=params, 
            auth=('apikey', WATSON_KEY['key']))
        response = json.loads(response.text)
        return response

_delete_session()
#import requests

#headers = {
    #'Content-Type': 'application/json',
#}

#params = (
 #   ('version', '2019-02-28'),
#
# )

#data = '{"input": {"text": "Hello"}}'

#response = requests.post('{}/v2/assistants/{}/sessions/{}/message', headers=headers, params=params, data=data, auth=('apikey', '{apikey}'))
