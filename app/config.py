import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gizli_anahtar'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:asdasd123@localhost:5432/scoreboard_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
