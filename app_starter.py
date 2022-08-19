from flask_migrate import Migrate
from app_racine import create_app
from app_racine import database as db
from app_racine.users.models import *
from app_racine.master.models import *
from app_racine.mosque.models import *
from app_racine.donors.models import *

import os

from dotenv import load_dotenv

load_dotenv('.flaskenv')
app = create_app(os.environ.get('FLASK_ENV'))

migrate = Migrate(app=app, db=db)

@app.shell_context_processor
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
