from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager, Server
from app_racine import create_app, db
from app_racine.users.models import *
from app_racine.master.models import *
from app_racine.mosque.models import *
from app_racine.donors.models import *

import os

app = create_app(os.environ.get('FLASK_ENV'))
manager = Manager(app)

migrate = Migrate(app, db, render_as_batch=True)


def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                DonateMosque=DonateMosque,
                Mosque=Mosque,
                Garant=Garant,
                Personne=Personne,
                SituationGarant=SituationGarant,
                SituationPerson=SituationPerson,
                Critere=Critere,
                ParameterUtils=ParameterUtils,
                Participe=Participe,
                Project=Project,
                GarantProject=GarantProject,
                )


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
if __name__ == "__main__":
    manager.run()
