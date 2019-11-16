from flask_restful import Resource, reqparse
from flask import jsonify
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    jwt_required, 
    fresh_jwt_required, 
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST

_parser =reqparse.RequestParser()
_help = "This field is required"
_parser.add_argument("username", type=str, required=True, help=_help)
_parser.add_argument("password", type=str, required=True, help=_help)

errorMessage=  {
    "code" : "404",
    "message" : "Not found"
}

class User(Resource):
    @jwt_required
    def get(self):
        data = _parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user:
            return jsonify(user.json()), 200

        errorMessage['code'] = 404
        errorMessage['message'] = "User does not exist"
        return jsonify(errorMessage), 404

class UserRegistry(Resource):

    def post(self):
        data = _parser.parse_args()
        user = UserModel.find_by_username(data['username'])        
        if user:
            errorMessage['code'] = 400
            errorMessage['message'] = "Username is taken"
            return jsonify(errorMessage), 400
        print(data)
        user = UserModel(**data)
        user.save_to_db()
        print(user.json())
        return jsonify(user.json()), 201

class UserLogin(Resource):

    def post(self):
        data = _parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            return jsonify({
                    "access_token" : create_access_token(identity=user.id, fresh=True),
                    "refresh_token" : create_refresh_token(user)
                }), 201

        errorMessage['code'] = 404
        errorMessage['message'] = "User not found, please register"
        return jsonify(errorMessage), 404

class FreshToken(Resource):
    
    @jwt_refresh_token_required
    def post(self):
        user_id = get_jwt_identity()
        if UserModel.find_by_id(id=  user_id):
            return jsonify({"access_token" : create_access_token(identity=user_id, fresh=False)})
        
        errorMessage['code'] = 404
        errorMessage['message'] = "User does not exist"
        return jsonify(errorMessage), 404
    

class UserLogout(Resource):

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return jsonify({"message": "User logout successfully"}),200
