from flask import Blueprint

mosque_bp = Blueprint('mosque_bp', __name__, url_prefix="/mosque")

from app_racine.mosque import models, routes