import boto3
import hmac
import hashlib
import base64


def get_secret_hash(username):
    msg = username + '623vnb06drds7h0qquvti7o63i'
    dig = hmac.new(str('vqclgnm9qri6k3gdmt1328j3drrh63unsq03l3vsirnu0dv01s6').encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    print(d2)
    return d2


client = boto3.client('cognito-idp', region_name='us-east-1')


class CognitoService():
    def __init__(self) -> None:
        self.APPLICATION_ID = '623vnb06drds7h0qquvti7o63i'
        self.SERCRET_HAST = 'vqclgnm9qri6k3gdmt1328j3drrh63unsq03l3vsirnu0dv01s6'
        self.REGION_NAME = 'us-east-1'

    def signIn(self, **kwargs):

        return client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId='623vnb06drds7h0qquvti7o63i',
            AuthParameters={
                "PASSWORD": kwargs['password'],
                "USERNAME": kwargs['username'],
                "SECRET_HASH": get_secret_hash(kwargs['username'])
            }
        )

    def signUp(self, **kwargs):
        print(kwargs)
        return client.sign_up(
            ClientId='623vnb06drds7h0qquvti7o63i',
            SecretHash=get_secret_hash(kwargs['username']),
            Username=kwargs['username'],
            Password=kwargs['password'],
            UserAttributes=[
                {
                    'Name': 'email', 'Value': kwargs['email']},
            ]
        )

    def verify(self, **kwargs):
        return client.confirm_sign_up(
            ClientId='623vnb06drds7h0qquvti7o63i',
            ConfirmationCode=kwargs['code'],
            SecretHash=get_secret_hash(kwargs['username']),
            Username=kwargs['username']
        )
