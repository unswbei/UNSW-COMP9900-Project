#!/usr/bin/python3
from time import time
import jwt
from itsdangerous import SignatureExpired

class AuthToken:
    """The auth token class, provide a HS256 based auth token"""
    def __init__(self, secret, expire):
        self.secret = secret
        self.expire = expire

    def decode(self, token):
        """Decode a token to its normal dictionary format
        Params:
        token -- a jwt HS256 auth_token string
        Return:
        decoded information in its original format
        """
        return jwt.decode(token, self.secret, algorithm='HS256')

    def token(self, userinfo):
        """Generate a auth token from user info
        Param:
        userinfo -- A userinfo dictionary from Admin/Dreamer/Collaborator info function
        Return:
        A jwt HS256 encoded token string
        """
        info = {'email': userinfo['email'], 'id': userinfo['id'], 'role': userinfo['role'], 'time': time()}
        return jwt.encode(info, self.secret, algorithm='HS256')

    def validate(self, token):
        """Validate a token to check if it has expired
        Param:
        token -- A jwt HS256 encoded token string
        Return:
        decoded information in its original format
        Exception:
        SignatureExpiredException
        """
        info = jwt.decode(token, self.secret, algorithm='HS256')
        if time() - info['time'] > self.expire:
            raise SignatureExpired("The token has been expired")
        return info

    def refresh(self, token):
        """Refresh a token expiration time
        Param:
        token -- A jwt HS256 encoded token string
        Return:
        A jwt HS256 encoded token string with new expiration time
        """
        info = self.validate(token)
        info['time'] = time()
        return jwt.encode(info, self.secret, algorithm='HS256')
