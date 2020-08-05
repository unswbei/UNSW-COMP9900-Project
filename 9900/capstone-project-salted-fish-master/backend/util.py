#!/usr/bin/python3

import re
from flask_restplus import Resource

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(file):
    """Check if the upload file is allowed in server"""
    return '.' in file and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_email_local(local):
    """Check the local part of email address in correct format"""
    pattern = '^([a-zA-Z0-9]([-]*[a-zA-Z0-9])*[\\.])*[a-zA-Z0-9]([-]*[a-zA-Z0-9])*$'
    valid = re.findall(pattern, local)
    return len(valid)

def check_email_domain(domain):
    """Check the domain part of email address in correct format"""
    pattern = '^([a-zA-Z0-9]([-]*[a-zA-Z0-9])*[\\.])+[a-zA-Z0-9]([-]*[a-zA-Z0-9])*$'
    valid = re.findall(pattern, domain)
    return len(valid)

def check_email(email):
    """Check the email address is valid"""
    email_split = email.split('@', 1)
    return check_email_local(email_split[0]) and check_email_domain(email_split[1])

class CorsResource(Resource):
    """Extend normal Resource class to allow Cors"""
    def options(self):
        """Cors option method"""
        return {'Allow': '*'}, 200, {'Access-Control-Allow-Origin': '*',
                                     'Access-Control-Allow-Methods': 'HEAD, OPTIONS, GET, POST, DELETE, PUT',
                                     'Access-Control-Allow-Headers': 'Content-Type, Content-Length, Authorization, Accept, X-Requested-With, Auth_Key'
                                    }
