from logging import getLogger, DEBUG, Formatter, StreamHandler
from flask_jwt_extended import JWTManager
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask import Flask, request, render_template
from flask_cors import CORS
from apispec import APISpec
from os.path import isfile
from os import getenv
from sys import stdout
import mysql.connector

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
while True:
    try:
        database = mysql.connector.connect(host = getenv('DB_HOST', 'db'),
                                           user = getenv('DB_USER', 'flask'),
                                           password = getenv('DB_PASSWORD', 'example'),
                                           port = 3306,
                                           database = getenv('DB_NAME', 'appdb'))
        break
    except Exception as e:
        print(f'{e}')


app.config['SECRET_KEY'] = 'anykey'


jwt = JWTManager(app)
docs = FlaskApiSpec()
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='NEWScrapper',
        version='v1.0',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/'
})


def setup_logger():
    log = getLogger(__name__)
    log.setLevel(DEBUG)

    handler = StreamHandler(stdout)
    handler.setLevel(DEBUG)
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log

logger = setup_logger()
