import os

class Config(object):
	SESSION_COOKIE_SAMESITE = "None"
	SESSION_COOKIE_SECURE = True
	SECRET_KEY = os.urandom(50).hex()
	SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
	UPLOAD_FOLDER = "/app/application/static/uploads"

class ProductionConfig(Config):
	pass

class DevelopmentConfig(Config):
	DEBUG = False

class TestingConfig(Config):
	TESTING = False
