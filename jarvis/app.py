from flask import Flask 
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.user import User, UserRegistry, UserLogin, FreshToken, UserLogout
from resources.jarvis import JARVIS
from blacklist import BLACKLIST


app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
	db.create_all()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = "example"

errorBody = {"code":0, "message": ""}

@jwt.token_in_blacklist_loader
def check_if_in_blacklist_callback(decrypted_key):
    return decrypted_key['jti'] in BLACKLIST

@jwt.unauthorized_loader
def unauthorized_callback(error):
    errorBody['code'] = 401
    errorBody['message'] = "Authorised token - please login"
    return errorBody, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    errorBody['code'] = 400
    errorBody['message'] = "Invalid token id - please register / login"
    return errorBody, 400

@jwt.expired_token_loader
def expired_token_callback():
    errorBody['code'] = 401
    errorBody['message'] = "Token expired - please login"
    return errorBody, 401

@jwt.revoked_token_loader
def revoke_access_callback():
    errorBody['code'] = 401
    errorBody['message'] = "User logout - please login"
    return errorBody, 401



api.add_resource(User, "/jarvis/user")
api.add_resource(UserRegistry, "/jarvis/register")
api.add_resource(UserLogin, "/jarvis/login")
api.add_resource(FreshToken, "/jarvis/token-refresh")
api.add_resource(UserLogout, "/jarvis/logout")
api.add_resource(JARVIS, "/jarvis/send-message")



if __name__ == "__main__":
    db.init_app(app)
    app.run(host="0.0.0.0")