class Config(object):
    DEBUG = True
    SECRET_KEY = "nbmxmVlanyiCum15prqNn5B1aw/uawQai8zkr5h+q1Eg8cbTtkOKCIluevwFLLvNhc62hP6ZN8C/wjNJqD7vZg=="
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db'
    CACHE_TYPE = "redis"
    SECURITY_PASSWORD_SALT = '123123123123123dzbdgmjhzfgjdgmdhmdhjdmhdfgh'
    MAIL_SERVER = 'mail.cock.li'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = DEBUG
    MAIL_USERNAME = 'librenotes@airmail.cc'
    MAIL_PASSWORD = 'librenotes2018*'
    MAIL_DEFAULT_SENDER = 'librenotes@airmail.cc'


class ProductionConfig(Config):
    MAIL_SUPPRESS_SEND = False
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@51.15.69.117/bal_yeni"
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/bal_yeni"
