from flask import url_for, redirect, request, render_template, abort, session

from app_racine.donors.models import *
from flask_login import current_user, login_required

from app_racine.donors import donor_bp


@donor_bp.route('/donor_dashboard', methods=['GET', 'POST'])
@login_required
def donor_dashboard():
    return "donor dashboard"
