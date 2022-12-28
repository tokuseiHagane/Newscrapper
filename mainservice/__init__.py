from .controllers.SetupController import app, docs, jwt
from .controllers.ViewsController import views

app.register_blueprint(views)
docs.init_app(app)
jwt.init_app(app)
