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
        access_token = USER_KEY.get("access_token")
        self._create_session()
        if access_token == "" or access_token is None:
            pass

    def retrieve_access_token(self):
        url = USER_KEY['auth_url']
        headers = {"Content-Type" : "application/x-www-form-urlencoded", "Accept": "application/json"}
        data = {"apikey" : WATSON_KEY['key'], "grant_type" : "urn:ibm:params:oauth:grant-type:apikey"}
        response = requests.post(url, data, headers= headers)
        if response.code == 200 or response.code == 201:
            print("Access_token retrieved")
            response = response.get_json()
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

    def _create_session(self):
        base_url = WATSON_KEY['url']
        assistant_id = WATSON_KEY['assistant_id']
        completeUrl = "{}/v2/assistants/{}/sessions?version=2019-02-28".format(base_url, assistant_id)
        data = {"apikey" : WATSON_KEY['key']}
        headers = {"Content-Type" : "application/x-www-form-urlencoded"}
        response = requests.post(completeUrl, data, headers=headers)
        response = response.get_json()
        session_id = response.get("session_id")
        if session_id :
            USER_KEY["session_id"] = session_id
            print("Session with IBM Watson created")
            return True
        print("Session problem")
        return False

    def _delete_session(self):
        url = "{}/v2/assistants/{}/sessions/{}?version=2019-02-28".format(WATSON_KEY['url'], WATSON_KEY['assistant_id'], USER_KEY['session_id'])
        data = {"apikey" : WATSON_KEY['key']}
        headers = {"Content-Type" : "application/x-www-form-urlencoded"}
        response = requests.post(url, data, headers=headers)
        if response.code == 200:
            print("Session deleted")
            return True
        print("Session delete - Error")
        return False

    def send_message(message):
        pass



    