from flask import Blueprint

master_bp = Blueprint('master_bp', __name__, url_prefix='/master')

from app_racine.master import routes