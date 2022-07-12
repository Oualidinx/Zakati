from flask import Blueprint

donor_bp = Blueprint('donor_bp', __name__, url_prefix="/donor")

from app_racine.donors import routes