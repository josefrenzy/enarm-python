from flask import Flask
from flask_restx import Resource, Api, reqparse

import boto3
import hmac
import hashlib
import base64

app = Flask(__name__)
api = Api(app)


def get_secret_hash(username):
    msg = username + '623vnb06drds7h0qquvti7o63i'
    dig = hmac.new(str('vqclgnm9qri6k3gdmt1328j3drrh63unsq03l3vsirnu0dv01s6').encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    print(d2)
    return d2


client = boto3.client('cognito-idp', region_name='us-east-1')


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/auth/signin')
class Auth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        kwargs = parser.parse_args()
        r = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId='623vnb06drds7h0qquvti7o63i',
            AuthParameters={
                "PASSWORD": kwargs['password'],
                "USERNAME": kwargs['username'],
                "SECRET_HASH": get_secret_hash(kwargs['username'])
            }
        )
        return r


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
        args = parser.parse_args()
        print(args['email'])
        # print('some over here', args)
        r = client.sign_up(
            ClientId='623vnb06drds7h0qquvti7o63i',
            SecretHash=get_secret_hash(args['username']),
            Username=args['username'],
            Password=args['password'],
            UserAttributes=[
                {
                    'Name': 'email', 'Value': args['email']},
            ]
        )
        print("--------------------", r)
        return r


@api.route('/auth/verify')
class Auth(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('code')
        kwargs = parser.parse_args()
        r = client.confirm_sign_up(
            ClientId='623vnb06drds7h0qquvti7o63i',
            ConfirmationCode=kwargs['code'],
            SecretHash=get_secret_hash(kwargs['username']),
            Username=kwargs['username']
        )

        return r


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
