from cred import USER_KEY, WATSON_KEY
import requests
class Message():
    def __init__(self, message_type, text):
        self.message_type = message_type
        self.text = text

    def json(self):
        return {"message_type" : self.message_type, "text" : self.text}

class JarvisModel():
    def __init__(self):
        pass

    def retrieve_access_token():
        url = USER_KEY['auth_url']
        headers = {"Content-Type" : "application/x-www-form-urlencoded", "Accept": "application/json"}
        data = {"apikey" : WATSON_KEY['key'], "grant_type" : "urn:ibm:params:oauth:grant-type:apikey"}
        response = requests.post(url, data, headers= headers)
        print(response)
        if response.status_code == 200 or response.status_code == 201:
            print("Access_token retrieved")
            response = json.loads(response.text)
            USER_KEY['access_token'] = response['access_token']
            USER_KEY['refresh_token'] = response['refresh_token']
            return True
        print("Access-token extraction failed")

    def refresh_access_token(self):
        url = USER_KEY['auth_url']
        headers = {"Authorization" : "Basic Yng6Yng="}
        data = {"grant_type" : "refresh_token","refresh_token": USER_KEY['refresh_token']}
        response = requests.post(url, data, headers=headers)
        response = response.get_json()
        access_token = response.get("access_token")
        if access_token != "" or access_token is not None:
            USER_KEY['access_token']= access_token
            print("access token is refreshed")
            return True
        print("Error while refreshing the token")
        return False

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

    def send_message(message):
        session = _create_session()
        print(session)
        data = {
            "input": {
                "text": message
            }
        }
        #_auth = ('apikey',WATSON_KEY['key'])
        params = (('version', '2019-02-28'),)
        headers = {"Content-Type": "application/json"}
        url = WATSON_KEY['assistant_url']+"/{}/message".format(session)
        print(url)
        response = requests.post(url, headers=headers, params=params, data=json.dumps(data), auth=('apikey', WATSON_KEY['key']))
        res = json.loads(response.text)
        return res


