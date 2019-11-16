from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.jarvisAssistant import JARVISModel


class JARVIS(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("message", type=str, required=True, help="This field is required")

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        result = JARVISModel.sendMessage(data['message'])
        if result:
            return result, 200
        return {"message" : "Internal server error"}, 500
