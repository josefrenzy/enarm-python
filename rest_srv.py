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


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@api.route('/auth/signin')
class Auth(Resource):
    def post(self):
        pass


@api.route('/auth/signup')
class Auth(Resource):

    # def __init__(self):
    #     """
    #     :param cognito_idp_client: A Boto3 Amazon Cognito Identity Provider client.
    #     :param user_pool_id: The ID of an existing Amazon Cognito user pool.
    #     :param client_id: The ID of a client application registered with the user pool.
    #     :param client_secret: The client secret, if the client has a secret.
    #     """

    #     self.user_pool_id = 'us-east-1_Px7zurHIM'  # user_pool_id
    #     self.client_id = '623vnb06drds7h0qquvti7o63i'  # client_id
    #     self.client_secret = 'vqclgnm9qri6k3gdmt1328j3drrh63unsq03l3vsirnu0dv01s6'  # client_secret

    def post(self):
        client = boto3.client('cognito-idp')
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
        return args


@api.route('/auth/verify')
class Auth(Resource):
    def post(self, operation):
        pass


# @api.route('/auth/')
# class Auth(Resource):
#     def post(self, operation):
#         if (operation == 'sigin'):
#             pass
#         elif (operation == 'signup'):
#             pass
#         elif (operation == 'verify'):
#             pass
#         elif (operation == 'forgotpass'):
#             pass
#         elif (operation == 'confirmpass'):
#             pass


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
