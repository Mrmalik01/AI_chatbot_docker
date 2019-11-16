# AI_chatbot_docker

Chatbot as a service - It allows user to communicate with IBM-Watson personal assistant using simple interface. 

## Installation

Before building and running the service, you need to create one file jarvis/cred.py of given format

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

## Steps for interacting with the bot

<ol>
    <li>Register with username and password</li>
    <li>Login with username and password</li>
    <li>Send message using send end point</li>
</ol>

Enjoy!!
