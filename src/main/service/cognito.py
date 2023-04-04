import boto3
import hmac
import hashlib
import base64

from logger.app_logging import getlogger
from config.constants import EnvVar

logger = getlogger(__name__)


def get_secret_hash(username):
    msg = username + EnvVar.CLIENT_ID
    dig = hmac.new(str(EnvVar.SECRET_HASH).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


client = boto3.client('cognito-idp', region_name=EnvVar.REGION_NAME)


class CognitoService(object):
    def __init__(self) -> None:
        self.application_id = EnvVar.CLIENT_ID

    def signIn(self, **kwargs):
        logger.debug(kwargs)
        return client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=str(EnvVar.CLIENT_ID),
            AuthParameters={
                "PASSWORD": kwargs['password'],
                "USERNAME": kwargs['username'],
                "SECRET_HASH": get_secret_hash(kwargs['username'])
            }
        )

    def signUp(self, **kwargs):
        logger.debug(kwargs)
        return client.sign_up(
            ClientId=str(EnvVar.CLIENT_ID),
            SecretHash=get_secret_hash(kwargs['username']),
            Username=kwargs['username'],
            Password=kwargs['password'],
            UserAttributes=[
                {
                    'Name': 'email', 'Value': kwargs['email']},
            ]
        )

    def verify(self, **kwargs):
        logger.debug(kwargs)
        return client.confirm_sign_up(
            ClientId=str(EnvVar.CLIENT_ID),
            ConfirmationCode=kwargs['code'],
            SecretHash=get_secret_hash(kwargs['username']),
            Username=kwargs['username']
        )
