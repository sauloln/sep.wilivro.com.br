import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "troque-esta-chave")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///sep.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")

    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "static/uploads")

    # Visual defaults
    APP_TITLE = os.environ.get("APP_TITLE", "SEP - Sistema de Estoque e Patrimônio")
