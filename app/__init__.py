from flask import Flask
from .extensions import db, login_manager, socketio
#from .routes import main
from .routes import routes
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", async_mode='threading', transports=["polling"])

    app.register_blueprint(routes)

    return app
