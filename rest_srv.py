from flask import Flask
from flask_restx import Resource, Api, reqparse
from botocore.exceptions import ClientError

from main.src.service import cognito
from main.src.logger.app_logging import getlogger

from main.src.config.constants import FlaskConfig

logger = getlogger(__name__)

app = Flask(__name__)
api = Api(app)


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/auth/signin')
class Auth(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username')
            parser.add_argument('password')
            kwargs = parser.parse_args()
            r = cognito.CognitoService.signIn(self, **kwargs)
            return r
        except ClientError as e:
            print(e.response['Error']['Code'])
            if (e.response['Error']['Code'] == "NotAuthorizedException"):
                logger.debug(e.response)
                return {
                    "errorCode": e.response['Error']['Code'],
                    "statusCode": 403,
                    "message": "Nombre de usuario o Contraseña no validos"}


@api.route('/auth/signup')
class Auth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('email')
        parser.add_argument('birthdate')
        parser.add_argument('family_name')
        parser.add_argument('password')
        parser.add_argument('phone_number')
        parser.add_argument('name')
        parser.add_argument('status')
        parser.add_argument('subscription_end')
        parser.add_argument('subscription_start')
        parser.add_argument('study_plan')
        parser.add_argument('type_user_id')
        kwargs = parser.parse_args()
        try:
            return cognito.CognitoService.signUp(self, **kwargs)
        except ClientError as e:
            if (e.response['Error']['Code'] == "UsernameExistsException"):
                logger.debug(e.response)
                return {
                    "errorCode": e.response['Error']['Code'],
                    "statusCode": 409,
                    "message": "El usuario que intentas registrar ya existe"}


@api.route('/auth/verify')
class Auth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('code')
        kwargs = parser.parse_args()
        try:
            return cognito.CognitoService.verify(self, **kwargs)
        except ClientError as e:
            if (e.response['Error']['Code'] == "ExpiredCodeException"):
                logger.debug(e.response)
                return {
                    "errorCode": e.response['Error']['Code'],
                    "statusCode": 405,
                    "message": "Codigo de verificacion Vencido"}


if __name__ == '__main__':
    app.run(debug=True, port=FlaskConfig.Port, host=FlaskConfig.Host)
