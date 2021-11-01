class Config:
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
    SECRET_KEY='69ae5bd0ce7c457caf8ac853d9484e176e03f0af777158259de72c2fce40ae273a08b76b1aa161591a57b13a36807bfc089b1d08db816aaf32775c79a3eea344d88ff6578e84a48be667097b8ec3d14eff9ce2323cfbc95abbb936db4e651354aef0a43dd60cf0de95678c17908d343cb505bf82abdb41d4661da8ed61187798'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///data-test.db"
    SECRET_KEY='4d3add65ad8f19e70dffc8adc956f7178ed70873bdd669938b6ce0980f463410152a64a3e37ba0c660c28844257f3ae77a04497aed8e91c962a6eb283ded27e4'


class ProductionConfig(Config):
    SECRET_KEY = "c49908a9a617b188b4feaacaf927a184f329412d91e47a950bf1c1641ff6f11929981a93614b6dd6832c6cd0a65c711e4416b89c5da40635b7cab05b25b183656b69fdf0b9fc3ad0026a1327c6a63e657db9d2fdddf05038e6a6d54fd9b818e00c78020d37fbc303026d111354bd5681f52653e7da891130db6365caf44424e3628126dfbd5120a81386cded38170cebf5a722f89477d9df17cf42a1411c1a320f7c88b7ec2806ad5885dbbc5173e86d025cc44b348575bdf2a607caf352f0e1690361481199c1fa87b301a5c0041017d2292cc2c37181e69010a20355641baa377a4dd7abab9df5c65419b0afd8fccb4fdc0f413a890380e2f00238a9252b2f"
    SQLALCHEMY_DATABASE_URI = "postgresql://ipqtwvvdpvnibn:a0aea41e92da88c0f650cca92f9852710f5f0706ac0b4f46e46d5c1b2e850f7d@ec2-3-228-86-183.compute-1.amazonaws.com:5432/d6uib57pifhtqk"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
