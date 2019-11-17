from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.jarvis import JarvisModel


parser = reqparse.RequestParser()
parser.add_argument("message", type=str, required=True, help="This field is required")

class JARVIS(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        if data.get("message") is None or data.get("message") == "":
            return {"message":"please enter a message "}, 400

        result = JarvisModel.send_message(data['message'])
        if result:
            return result, 200
        return {"message" : "Internal server error"}, 500
