import os

PWD = os.path.abspath(os.curdir)
DEBUG = False


class Config(object):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    SECRET_KEY = 'dhsfegjkrebdfkjheo'
    SESSION_PROTECTION = 'strong'
    SECURITY_PASSWORD_SALT = 'kjdheidubfduewy8eweuuhdj9^^*W@EhfkjadfbdbIJ(&EYEdaKEJ@E(*@!qejb'


class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://mbkodzmdestiaq:41e8a8a6b37f0170f6d567918d376f75c1f40d14e86841feace6db5a54f3089c@ec2-54-235-45-88.compute-1.amazonaws.com:5432/d34k33c6a3679v"

    ENVIRONMENT = 'production'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgres://ritwick:ritwickasha@localhost:5432/scaler"

    ENVIRONMENT = 'development'


config = {
    "production": "api.config.ProductionConfig",
    "development": "api.config.DevelopmentConfig",
    "default": "api.config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'development')
    print(config_name)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    app.config['type'] = config_name
