import secrets
from app_racine.mosque import mosque_bp

from app_racine.mosque.forms import *

from app_racine.donors.models import *

from app_racine.authentication.forms import *
from flask_login import login_required, current_user
from flask import redirect, render_template, request, \
    session, flash, abort, url_for
from werkzeug.security import generate_password_hash
from app_racine.utils import *


@mosque_bp.before_request
def mosque_before_request():
    if current_user.is_authenticated and current_user.role == 'imam':
        session['mosque_name'] = Mosque.query.filter_by(user_account=current_user.id).first().nom
    else:
        abort(403)


@mosque_bp.route("/printTablePDF/<int:project_id>")
@login_required
def PrintTable(project_id):
    temp = Mosque.query.filter_by(user_account=current_user.id).first()
    if temp:
        return temp.PrintResume(project_id)
    abort(404)


@mosque_bp.route('garant/<int:_id>/form')
@login_required
def PrintForm(_id):
    garant = Garant.query.get(_id)
    if garant:
        return garant.print_form()
    abort(404)


@mosque_bp.route('/mosque/dashboard', methods=['GET', 'POST'])
@login_required
def mosque_dashboard():
    mosque = Mosque.query.filter_by(user_account=current_user.id).first()
    if not mosque:
        abort(404)
    else:
        donation = DonateMosque.query.filter_by(mosque_id=mosque.id).all()
        donations = [user.user_id for user in donation] if donation else None
        return render_template(
            'mosque/mosque.html',
            donors=len(list(dict.fromkeys(donations))) if donations else 0,
            sum_donates=sum([don.amount for don in mosque.donors]),
            mosque=mosque.to_dict(),
            tendancy=Mosque.get_value(),
            nbre_inscrits=len(mosque.inscrits) if mosque.inscrits else 0
        )


@mosque_bp.route('/garants/new', methods=['GET', 'POST'])
@login_required
def register_garants():
    form = RegisterGarantForm()
    famille = PersonPerGarant()
    form.situation_sante.choices = [(x.id, x.label) for x in
                                    Critere.query.filter_by(category='الصحية').all()]
    form.situation_sociale.choices = [(x.id, x.label) for x in
                                      Critere.query.filter_by(
                                          category='الاجتماعية').all()]
    form.situation_familliale.choices = [(x.id, x.label) for x in
                                         Critere.query.filter_by(
                                             category='العائلية').all()]
    membre = Mosque.query.filter_by(user_account=current_user.id).first()
    if form.validate_on_submit():
        garant = Garant()
        garant.ccp = form.compte_ccp.data
        garant.cle_CCP = form.cle_ccp.data
        garant.prenom = form.prenom.data
        garant.nom = form.nom.data
        garant.address = form.address.data
        garant.phone_number = form.phone_number.data
        garant.date_nais = form.date_nais.data
        garant.num_extrait_nais = form.num_extrait_nais.data
        garant.mosque_id = membre.id
        liste = request.form.getlist('situation_sociale') + request.form.getlist(
            'situation_familliale') + request.form.getlist('situation_sante')
        db.session.add(garant)
        db.session.commit()
        for case in liste:
            status = SituationGarant()
            status.garant_id = garant.id
            status.critere_id = int(case)
            db.session.add(status)
            db.session.commit()
        person = Personne()
        person.nom = famille.p_nom.data
        person.prenom = famille.p_prenom.data
        person.date_naissance = famille.p_date_nais.data
        person.relation_ship = famille.p_relation_ship.data
        person.garant_id = garant.id
        db.session.add(person)
        db.session.commit()
        if famille.handicap.data:
            handicap = SituationPerson()
            handicap.personne_id = person.id
            handicap.critere_id = Critere.query.filter_by(label="اعاقة").first().id
            db.session.add(handicap)
            db.session.commit()

        if famille.education.data:
            education = SituationPerson()
            education.personne_id = person.id
            education.critere_id = Critere.query.filter_by(label="فرد متمدرس").first().id
            db.session.add(education)
            db.session.commit()

        if famille.malade_cronic.data:
            malade_cronic = SituationPerson()
            malade_cronic.personne_id = person.id
            malade_cronic.critere_id = Critere.query.filter_by(label="مرض مزمن").first().id
            db.session.add(malade_cronic)
            db.session.commit()

        if int(request.form['max_clicks']) != 0:
            final_test = get_data_from_request(request, garant.id)
            if not final_test:
                flash('لقد تم تسجيل مكفول تم تسجيله من قبل ككفيل', 'danger')
                return redirect(url_for('mosque_bp.register_garants'))
        count_points(garant, famille)
        db.session.add(garant)
        db.session.commit()
        Mosque.tendance()
        flash("لقد تم اضـــــافة الفرد بنجاح", "success")
        return redirect(url_for('mosque_bp.register_garants'))
    return render_template('mosque/register_G.html', famille=famille, form=form)


@mosque_bp.route("/donations/new", methods=['GET', 'POST'])
@login_required
def register_donation():
    form = RegisterNewDonationForm()
    form.project.choices = [(x.id, x.title) for x in Project.query.all()]
    membre = Mosque.query.filter_by(user_account=session['user_id']).first()
    if form.validate_on_submit():
        operation = DonateMosque()
        operation.mosque_id = membre.id
        user = User.query.filter_by(phone_number=form.phone_number.data).first()
        if not user:
            user = User()
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.phone_number = form.phone_number.data
            user.role = 'donor'
            user.username = str(secrets.token_hex(8))
            password_hash = generate_password_hash(str(secrets.token_hex(8)), 'sha256')
            user.password = password_hash
            db.session.add(user)
            db.session.commit()
        operation.user_id = user.id
        operation.amount = form.montant.data
        db.session.add(operation)
        db.session.commit()
        flash("تمت الاضافـــة بنجاح", "success")
        return redirect(url_for('mosque_bp.register_donation'))
    return render_template("mosque/register_don.html", form=form)


@mosque_bp.route("/mosque/donations/<int:page>")
@login_required
def list_dons(page):
    mosque = Mosque.query.filter_by(user_account=session['user_id']).first()
    if not mosque:
        abort(404)
    else:
        donations = DonateMosque.query.filter_by(mosque_id=mosque.id)
        data = DonateMosque.to_collection_dict(
            query=donations,
            page=page,
            per_page=12,
            edit_endpoint=None,
            list_endpoint="mosque_bp.list_dons",
            delete_endpoint=None,
            view_endpoint=None,
            columns=["رقم العملية", 'التاريـــخ', 'المتبرع', 'المبلــغ']
        )
        return render_template('mosque/list_dons.html', results=data)


@mosque_bp.route('/garant/<int:_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_garant(_id):
    garant = Garant.query.get(_id)
    if not garant:
        abort(404)
    else:
        if garant.is_active == 1:
            garant.is_active = 0
        elif garant.is_active == 0:
            garant.is_active = 1
        db.session.add(garant)
        db.session.commit()
        flash('تمت العملية بنجاح', 'success')
        return redirect(url_for('mosque_bp.list_garants', page=1))


@mosque_bp.route("/garants/<int:page>", methods=['GET', 'POST'])
@login_required
def list_garants(page):
    form = ProjectsSelectForm()
    form.projects.choices = [(-1, 'كل المجتاجيـن')] + [(x.id, x.title) for x in Project.query.all()]
    Mosque.tendance()
    data = None
    if form.validate_on_submit():
        prj = Project.query.get(int(form.projects.data))
        if int(form.projects.data == -1):
            data = Garant.to_collection_dict(
                query=Garant.query.join(Mosque, Mosque.id == Garant.mosque_id).filter(
                    Mosque.usser_account == current_user.id),
                page=page,
                per_page=12,
                edit_endpoint=None,
                delete_endpoint="mosque_bp.delete_garant",
                view_endpoint="mosque_bp.PrintForm",
                list_endpoint="mosque_bp.list_garants",
                columns=['الرقم', 'اسم الكفيل', 'لقب الكفيل', 'رصيد الأسهـم']
            )
        elif prj and prj.title == 'المنحة الشهرية':
            session['project_id'] = int(form.projects.data)
            data = Garant.to_collection_dict(
                query=Garant.query.join(Mosque, Mosque.id == Garant.mosque_id) \
                    .filter(Mosque.usser_account == current_user.id) \
                    .filter(is_concerned_prime_m(Garant.id) is not None),
                page=page,
                per_page=12,
                edit_endpoint=None,
                delete_endpoint="mosque_bp.delete_garant",
                view_endpoint="mosque_bp.PrintForm",
                list_endpoint="mosque_bp.list_garants",
                columns=['الرقم', 'اسم الكفيل', 'لقب الكفيل', 'مبلغ المنحة الشهرية', 'ت. الميلاد']
            )
        elif prj and prj.title == "منحة التمدرس":
            session['project_id'] = int(form.projects.data)
            data = Garant.to_collection_dict(
                query=Garant.query.join(Mosque, Mosque.id == Garant.mosque_id) \
                    .filter(Mosque.usser_account == current_user.id) \
                    .filter(is_concerned_prime_s(Garant.id) is not None),
                page=page,
                per_page=12,
                edit_endpoint=None,
                delete_endpoint="mosque_bp.delete_garant",
                view_endpoint="mosque_bp.PrintForm",
                list_endpoint="mosque_bp.list_garants",
                columns=['الرقم', 'اسم الكفيل', 'لقب الكفيل', 'مبلغ منحة التمدرس', 'ت. الميلاد']
            )
    return render_template('mosque/list_garants.html', results=data if data else None, form = form)


@mosque_bp.route("/donneur")
@login_required
def donneur():
    content = {
        'donneur': User.query.all(),
        'operations': DonateMosque.query.all()
    }
    return render_template('donneur.html', contents=content, title="زكـاة : متبرع")


@mosque_bp.route("/mosque/update", methods=['GET', 'POST'])
@login_required
def update_info():
    mosque = Mosque.query.filter_by(user_account=current_user.id).first()
    if not mosque:
        abort(404)
    else:
        user = User.query.get(current_user.id)
        form = UpdateAccountForm()
        if request.method == 'GET':
            form.email.data = user.email
            form.username.data = user.username
            form.phone_num.data = user.phone_number
            form.first_name.data = user.first_name
            form.last_name.data = user.last_name
        elif form.validate_on_submit():
            _user = User.query.filter_by(phone_number=form.phone_num.data).first()
            if not _user:
                _user = User()
            _user.first_name = form.first_name.data
            _user.last_name = form.last_name.data
            _user.email = form.email.data if form.email.data != '' else None
            _user.password = user.password
            _user.phone_number = form.phone_num.data
            _user.username = user.username
            db.session.add(_user)
            db.session.commit()

            mosque.user_account = _user.id
            db.session.add(mosque)
            db.session.commit()
            flash('تمت العملية بنجاح', 'success')
            return redirect(url_for('mosque_bp.update_info'))
        return render_template('mosque/update_info.html', form=form)


@mosque_bp.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = EditPasswordForm()
    user = User.query.get(current_user.id)
    mosque = Mosque.query.filter_by(user_account=user.id).first()
    if not user or not mosque:
        abort(404)
    else:
        if form.validate_on_submit():
            user.password = generate_password_hash(form.password.data, 'sha256')
            db.session.add(user)
            db.session.commit()
            flash('تمت العملية بنجاح', 'success')
            return redirect(url_for('mosque_bp.mosque_dashboard'))
        return render_template('mosque/update_password.html', form=form)


@mosque_bp.route('garant/by_project/<int:_id>', methods=['GET', 'POST'])
@login_required
def filter_by_project(_id):
    project = Project.query.get(_id)
    if not project:
        abort(404)
    else:
        session['project_id'] = project.id
        return redirect(url_for('mosque_bp.list_garants', page=1))
