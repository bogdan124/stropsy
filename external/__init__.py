import datetime
import jwt
from env_class import Env


def encode_auth_token(user_id,email):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=100, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id,
            "email":email
        }
        return jwt.encode(
            payload,
            Env().APP_SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token,Env().APP_SECRET_KEY)
        return (payload,200)
    except jwt.ExpiredSignatureError:
        return ('Signature expired. Please log in again.',404)
    except jwt.InvalidTokenError:
        return ('Invalid token. Please log in again.',404)
