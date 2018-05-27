class Config(object):
    DEBUG = True
    SECRET_KEY = "KEY"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db'
    CACHE_TYPE = "redis"
    SECURITY_PASSWORD_SALT = 'SALT'
    MAIL_SERVER = 'MAIL_SERVER'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = DEBUG
    MAIL_USERNAME = 'MAIL_USERNAME'
    MAIL_PASSWORD = 'MAIL_PASSWORD'
    MAIL_DEFAULT_SENDER = 'MAIL_SENDER@SENDER.COM'


class ProductionConfig(Config):
    MAIL_SUPPRESS_SEND = False
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:DB"
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:DB"
