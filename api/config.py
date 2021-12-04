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
    SQLALCHEMY_DATABASE_URI = "postgresql://olricustrkyuhv:2358591c636ea4962098dcd370f94c052b3b6deff114627572025749bb5f4335@ec2-3-230-219-251.compute-1.amazonaws.com:5432/db0rv0d296sg6"

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
    config_name = os.getenv('FLASK_CONFIGURATION', 'production')
    print(config_name)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    app.config['type'] = config_name
