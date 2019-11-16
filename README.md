# AI_chatbot_docker

## Installation

Before building and running the service, you need to create one file of jarvis/cred.py with given format

~~~
USER_KEY = {   
    "access_token" : "",
    "refresh_token ": "",
    "session_id" : "",
    "auth_url" : "https://iam.cloud.ibm.com/identity/token"
}

WATSON_KEY = {
    "key" : "", 
    "url" : "https://gateway-lon.watsonplatform.net/assistant/api",
    "assistant_id" : "",
    "assistant_name" : "",
    "assistant_url" : "",
    "version" : ""
}
~~~


## Building the service

~~~
docker-compose build
~~~

## Run the service

~~~
docker-compose up
~~~
