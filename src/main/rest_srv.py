
import json

from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Resource, Api, reqparse
from botocore.exceptions import ClientError

from service.cognito import CognitoService
from logger.app_logging import getlogger

from config.constants import FlaskConfig

from config.db_conn import DBUtils
from utils.common_utils import return_kwargs


logger = getlogger(__name__)

app = Flask(__name__)

# TODO wsgi add
CORS(app)
api = Api(app, doc='/api/v1/doc/', prefix='/api/v1')


# TODO implement health and ready endpoints

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
            r = CognitoService.signIn(self, **kwargs)
            return r
        except ClientError as e:
            if (e.response['Error']['Code'] == 'NotAuthorizedException'):
                logger.debug(e.response)
                return {
                    'errorCode': e.response['Error']['Code'],
                    'statusCode': 403,
                    'message': 'Nombre de usuario o Contraseña no validos'}


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
            return CognitoService.signUp(self, **kwargs)
        except ClientError as e:
            if (e.response['Error']['Code'] == 'UsernameExistsException'):
                logger.debug(e.response)
                return {
                    'errorCode': e.response['Error']['Code'],
                    'statusCode': 409,
                    'message': 'El usuario que intentas registrar ya existe'}


@api.route('/auth/verify')
class Auth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('code')
        kwargs = parser.parse_args()
        try:
            return CognitoService.verify(self, **kwargs)
        except ClientError as e:
            if (e.response['Error']['Code'] == 'ExpiredCodeException'):
                logger.debug(e.response)
                return {
                    'errorCode': e.response['Error']['Code'],
                    'statusCode': 405,
                    'message': 'Codigo de verificacion Vencido'}


@api.route('/payment')
class PaymentResource(Resource):
    du = DBUtils()

    def get(self):
        try:
            query = return_kwargs("get_payments")
            result = self.du.execute_query(query,)
            print(type(result))
            print(result)
            return {"status": "success", "data": result}
        except TypeError as te:
            logger.exception(te)
        except Exception as e:
            logger.exception(e)

    def post(self):
        pass


if __name__ == '__main__':
    app.run(debug=True, port=FlaskConfig.Port, host=FlaskConfig.Host)
