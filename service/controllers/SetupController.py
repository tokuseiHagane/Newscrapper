from logging import getLogger, DEBUG, Formatter, StreamHandler
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import JWTManager
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from apispec import APISpec
from os.path import isfile
from os import getenv
from sys import stdout
from flask_security import current_user, Security, SQLAlchemyUserDatastore


app = Flask(__name__)
# app.config.from_object(Config)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    getenv('DB_USER', 'flask'),
    getenv('DB_PASSWORD', 'example'),
    getenv('DB_HOST', 'db'),
    getenv('DB_NAME', 'appdb')
)
app.config['SECRET_KEY'] = 'anykey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

from models.DatabaseModels import Article, Media, MediaType, MediaSequence, SourceTag, SourceTags, Source, UrlType, Role, User

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

def error_handler(error):
    if isinstance(error, HTTPException):
        description = error.get_description(request.environ)
        code = error.code
        name = error.name
    else:
        description = ("We encountered an error "
                       "while trying to fulfill your request")
        code = 500
        name = 'Internal Server Error'
    template_to_try = '../view/errors/error{}.html'.format(code)
    if isfile(template_to_try):
        return render_template(template_to_try), code
    else:
        return render_template('../view/errors/generic_error.html'), code

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

class AnyPageView(BaseView):
    @expose('/')
    def any_page(self):
        return self.render('../admin/any_page/index.html')


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated()

admin = Admin(app, name='NEWScrapper DB', template_mode='bootstrap3', endpoint='admin', index_view=MyAdminIndexView())
admin.add_view(ModelView(Article, db.session, name='Статьи'))
admin.add_view(ModelView(Media, db.session, name='Список всех вложений'))
admin.add_view(ModelView(MediaType, db.session, name='Тип вложения'))
admin.add_view(ModelView(Source, db.session, name='Источники статей'))
admin.add_view(ModelView(MediaSequence, db.session, name='Вложения статей'))
admin.add_view(ModelView(SourceTag, db.session, name='Список тэгов'))
admin.add_view(ModelView(SourceTags, db.session, name='Тэги источника'))
admin.add_view(ModelView(UrlType, db.session, name='Тип источника'))
admin.add_view(AnyPageView(name='Что-то еще'))