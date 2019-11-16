from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.jarvis import JarvisModel


class JARVIS(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("message", type=str, required=True, help="This field is required")

    @jwt_required
    def post(self):
        data = self.parser.parse_args()
        print(data['message'])
        result = JarvisModel.send_message(str(data['message']))
        if result:
            return result, 200
        return {"message" : "Internal server error"}, 500
