import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, os.path.abspath('.flaskenv')))


class Config:
    SECRET_KEY = '105556cc73cea72e8673beb81ecbb19fb57c6db34f538aac0441908ed05967c73aa31054df224dffbbcbc24d' \
                 'd65f1bfda3ea8217bb183524216b26d39e5acd27 '
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REMEMBER_COOKIE_SECURE = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///data-dev.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///data-test.db"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://wyyvkwveqljivz:f48816285e283507b74155384c608731caea078425abde4e90e3c0a3d4fd561c@ec2-3-233-100-43.compute-1.amazonaws.com:5432/dfghls87d4dps1"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
