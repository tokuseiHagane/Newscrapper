from werkzeug.exceptions import default_exceptions
from controllers.SetupController import app, error_handler, docs, jwt

for exception in default_exceptions:
    app.register_error_handler(exception, error_handler)


#  from service.controller.db import db
#  app.register_blueprint(db)
#  from service.controller.views import views
#  app.register_blueprint(views)


docs.init_app(app)
jwt.init_app(app)
