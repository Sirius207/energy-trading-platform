import os
from flask import Flask, jsonify, make_response
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
from dotenv import load_dotenv

from config import db
from endpoints import RESOURCES


load_dotenv()


def create_app(config_mode):

    app = Flask(__name__)

    # pylint: disable=W0612
    @app.after_request
    def af_request(resp):
        resp = make_response(resp)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
        resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return resp

    # pylint: enable=W0612

    @app.errorhandler(Exception)
    def handle_error(error):

        code = 500

        if isinstance(error, HTTPException):
            code = error.code

        # pylint: disable=E1101
        app.logger.warning('{%d} - {%s}' % (code, error))
        # pylint: enable=E1101

        return jsonify(error=str(error)), code

    for ex in default_exceptions:
        app.register_error_handler(ex, handle_error)

    # flask config
    app.config.from_pyfile('./config/config.py')
    # pylint: disable=E1101
    app.logger.info('APP Mode: {%s}' % config_mode)
    # app.logger.info(f'APP Mode: {config_mode}')
    # pylint: enable=E1101

    # DB Init
    db.init_app(app)
    # Route Init
    api = Api(app)
    api.add_resource(RESOURCES['user'], '/user')
    api.add_resource(RESOURCES['login'], '/login')
    api.add_resource(RESOURCES['address'], '/address')
    api.add_resource(RESOURCES['amis'], '/amis')
    api.add_resource(RESOURCES['news'], '/news')
    api.add_resource(RESOURCES['power_info'], '/power_info')
    api.add_resource(RESOURCES['participant'], '/participant')
    api.add_resource(RESOURCES['bids'], '/bids')

    return app


def main():
    config_name = os.environ.get('APP_SETTINGS', 'development')
    app = create_app(config_name)
    app.run(
        host='0.0.0.0',
        port=os.environ.get('PORT', 5000)
        # ssl_context=app.config['SSL_CONTEXT'],
    )


if __name__ == "__main__":
    main()
