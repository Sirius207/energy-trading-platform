from flask import g, jsonify
from flask_httpauth import HTTPTokenAuth

from endpoints.user.model import User

# pylint: disable=C0103
auth = HTTPTokenAuth(scheme='Bearer')
# pylint: enable=C0103
@auth.verify_token
def verify_token(token):
    # get username and uuid from database
    user = User.query.filter_by(tag=token).first()
    if user:
        g.uuid = user.uuid
        g.account = user.account
        return True
    return False


@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401
