from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from cred import USER_KEY, WATSON_KEY
import json


class JARVISModel():
    
    @classmethod
    def authenticate(cls):
        authenticator = IAMAuthenticator('{}'.format(WATSON_KEY['key']))
        service = AssistantV2(
            version='2019-02-28',
            authenticator = authenticator
        )
        service.set_service_url(WATSON_KEY['url'])
        return service

    @classmethod
    def create_session(cls, service):
        response = service.create_session(assistant_id=WATSON_KEY['assistant_id']).get_result()
        res = json.dumps(response, indent=2)
        if "session_id" in res:
            USER_KEY['session_id'] = res.get("session_id")
            return service
            print("Session created")
        print("Session creation - failed")
        return None

    @classmethod
    def delete_session(cls, service):
        response = service.delete_session(
            assistant_id=WATSON_KEY['assistant_id'], 
            session_id = USER_KEY['session_id']).get_result()
        print(json.dumps(response, indent=2))
    
    @classmethod
    def sendMessage(cls, msg):
        service = cls.authenticate()
        service = cls.create_session(service)
        if service:
            response = service.message(
                assistant_id='{}'.format(WATSON_KEY['assistant_id']),
                session_id='{}'.format(USER_KEY['session_id']),
                input={
                    'message_type': 'text',
                    'text': msg
                }
            ).get_result()
            print(json.dumps(response, indent=2))
            print("Received the result")
            return str(response), 200

        else:
            print("Connection problem")
            return {"message" : "connection problem"}, 500


