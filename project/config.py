class Config(object):
    DEBUG = True
    SECRET_KEY="nbmxmVlanyiCum15prqNn5B1aw/uawQai8zkr5h+q1Eg8cbTtkOKCIluevwFLLvNhc62hP6ZN8C/wjNJqD7vZg=="
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db'
    CACHE_TYPE = "redis"


class ProductionConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@51.15.69.117/bal_yeni"
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/bal_yeni"
