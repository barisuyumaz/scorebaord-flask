from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'routes.login' # 'routes.' eklememizin sebebi login olmadan dashboard ve manage sayfalarına erişim olmaması için
socketio = SocketIO()

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

