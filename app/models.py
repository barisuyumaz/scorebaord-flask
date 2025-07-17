#Veritabanı modelleri
from .extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False) # string yapıldığında çok uzun versiyona çeviriyor
    role = db.Column(db.String(20), nullable=False)  # 'gorevli' veya 'hakem'


from datetime import datetime
class GameState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1_name = db.Column(db.String(50), default="Takım 1")
    team2_name = db.Column(db.String(50), default="Takım 2")
    team1_score = db.Column(db.Integer, default=0)
    team2_score = db.Column(db.Integer, default=0)
    minute = db.Column(db.Integer, default=0)
    second = db.Column(db.Integer, default=0)
    timer_running = db.Column(db.Boolean, default=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

