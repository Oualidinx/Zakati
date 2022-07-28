import secrets
from app_racine.mosque import mosque_bp

from app_racine.mosque.forms import *

from app_racine.donors.models import *

from app_racine.authentication.forms import *
from flask_login import login_required
from flask import redirect, render_template, request, \
    jsonify, flash, abort, url_for
from werkzeug.security import generate_password_hash
from app_racine.utils import *
from flask_weasyprint import HTML, render_pdf
from sqlalchemy.sql import and_


@mosque_bp.before_request
def mosque_before_request():
    if current_user.is_authenticated and current_user.role == 'imam':
        session['mosque_name'] = Mosque.query.filter_by(user_account=current_user.id).first().nom


# @mosque_bp.route("/printTablePDF/<int:project_id>")
@mosque_bp.route("/printTablePDF")
@login_required
# def PrintTable(project_id):
def print_table():
    garants = Garant.query.filter(Garant.mosque_id == Mosque.query.filter_by(user_account=current_user.id).first().id)
    data = dict()
    if garants:
        data['items'] = [dict(
            id=familly.id,
            first_name=familly.nom,
            last_name=familly.prenom,
            date_nais=familly.date_nais.date(),
            tendancy=familly.Solde_finale,
            solde=familly.get_total_sum(),
            id_card_number=familly.id_card_num
        ) for familly in garants.all()]
        data['number_g'] = len(garants.all())
        data['wilaya'] = Wilaya.query.get(Mosque.query.filter_by(user_account=current_user.id).first().state).name
        data['date'] = datetime.utcnow().date()
        data['title']=Mosque.query.filter_by(user_account = current_user.id).first().nom
        data['total'] = sum([f.Solde_part_financiere for f in garants.all()])
    else:
        data = None
    print(data)
    html = render_template('mosque/list.html', data=data)
    return render_pdf(HTML(string=html))

    # temp = Mosque.query.filter_by(user_account=current_user.id).first()
    # if temp:
    #     return temp.PrintResume(project_id)
    # abort(404)


@mosque_bp.route('/garant/<int:_id>/print')
@login_required
def print_form(_id):
    garant = Garant.query.get(_id)
    html = render_template(
        'mosque/form_temp.html',
        garant=garant.data(),
        title=Mosque.query.filter_by(user_account=current_user.id).first().nom
    )
    return render_pdf(HTML(string=html))


# @mosque_bp.route('garant/<int:_id>/form')
# @login_required
# def PrintForm(_id):
#     garant = Garant.query.get(_id)
#     if garant:
#         return garant.print_form()
#     abort(404)


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
    form.home_appliance.choices = [(x.id, x.label) for x in
                                   Critere.query.filter_by(category="الاجهزة الكهرومنزلية").all()]
    famille.situation.choices = [
        (state.id, state.label) for state in Critere.query.all()
    ]
    membre = Mosque.query.filter_by(user_account=current_user.id).first()
    if form.validate_on_submit():
        garant = Garant()
        garant.ccp = form.compte_ccp.data
        garant.id_card_num = form.card_id.data
        garant.id_card_release_date = form.release_date.data
        garant.id_card_release_authority = form.release_authority.data
        garant.cle_CCP = form.cle_ccp.data
        garant.prenom = form.prenom.data
        garant.nom = form.nom.data
        garant.address = form.address.data
        garant.phone_number = form.phone_number.data
        garant.date_nais = form.date_nais.data
        garant.num_extrait_nais = form.num_extrait_nais.data
        garant.mosque_id = membre.id
        liste = request.form.getlist('situation_sociale') + request.form.getlist(
            'situation_familliale') + request.form.getlist('situation_sante') + request.form.getlist('home_appliance')
        database.session.add(garant)
        database.session.commit()
        for case in liste:
            status = SituationGarant()
            status.garant_id = garant.id
            status.critere_id = int(case)
            database.session.add(status)
            database.session.commit()
        person = Personne()
        person.nom = famille.p_nom.data
        person.prenom = famille.p_prenom.data
        person.date_naissance = famille.p_date_nais.data
        person.relation_ship = famille.p_relation_ship.data
        person.garant_id = garant.id
        database.session.add(person)
        database.session.commit()
        # if famille.handicap.data:
        #     handicap = SituationPerson()
        #     handicap.personne_id = person.id
        #     handicap.critere_id = Critere.query.filter_by(label="اعاقة").first().id
        #     database.session.add(handicap)
        #     database.session.commit()
        if famille.cronic_desease.data:
            person.cronic_desease = famille.cronic_desease.data
            database.session.add(person)
            database.session.commit()
        if famille.situation.data:
            for state in request.form.getlist('situation'):
                _state = SituationPerson()
                _state.critere_id = int(state)
                _state.personne_id = person.id
                database.session.add(_state)
                database.session.commit()
        if int(request.form['max_clicks']) != 0:
            final_test = get_data_from_request(request, garant.id)
            if not final_test:
                flash('لقد تم تسجيل مكفول تم تسجيله من قبل ككفيل', 'danger')
                return redirect(url_for('mosque_bp.register_garants'))
        count_points(garant, famille)
        database.session.add(garant)
        database.session.commit()
        Mosque.tendance()
        flash("لقد تم اضـــــافة الفرد بنجاح", "success")
        return redirect(url_for('mosque_bp.register_garants'))
    else:
        print(form.errors)
        print(famille.errors)
    return render_template('mosque/register_G.html', famille=famille, form=form)


@mosque_bp.route('/api/situations', methods=['GET', 'POST'])
@login_required
def get_situation():
    response = [{'id': state.id, 'text': state.label} for state in Critere.query.all()]
    print(Critere.query.filter(Critere.label.like(f'%{request.args.get("search")}%')).all())
    if "search" in request.args:
        # print(f'search={get_display(arabic_reshaper.reshape(request.args.get("search")))}')
        response = [
            {'id': state.id, 'text': state.label} for state in
            Critere.query.filter(Critere.label.like(f'%{request.args.get("search")}%')).all()]
    return jsonify(response), 200


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
            database.session.add(user)
            database.session.commit()
        operation.user_id = user.id
        operation.amount = form.montant.data
        database.session.add(operation)
        database.session.commit()
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
        database.session.add(garant)
        database.session.commit()
        flash('تمت العملية بنجاح', 'success')
        return redirect(url_for('mosque_bp.list_garants', page=1))


@mosque_bp.route("/garants/<int:page>", methods=['GET', 'POST'])
@login_required
def list_garants(page):
    form = ProjectsSelectForm()
    form.projects.choices = [(-1, 'كل المجتاجيـن')] + [(x.id, x.title) for x in Project.query.all()]
    Mosque.tendance()
    data = Garant.to_collection_dict(
        query=Garant.query.filter(Garant.mosque_id == Mosque.query.filter_by(user_account=current_user.id).first().id),
        page=page,
        per_page=12,
        edit_endpoint=None,
        delete_endpoint="mosque_bp.delete_garant",
        view_endpoint="mosque_bp.print_form",
        list_endpoint="mosque_bp.list_garants",
        columns=['الرقم', 'اسم الكفيل', 'لقب الكفيل', 'مبلغ المنحة الشهرية', 'ت. الميلاد']
    )
    # print(f'{[t.to_dict() for t in data.all()]}')
    if form.validate_on_submit():
        prj = Project.query.get(int(form.projects.data))
        if prj and prj.title == 'المنحة الشهرية':
            session['project_id'] = int(form.projects.data)
            data = Garant.to_collection_dict(
                query=data.filter(is_concerned_prime_m(Garant.id) is not None),
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
                query=data.filter(is_concerned_prime_s(Garant.id) is not None),
                page=page,
                per_page=12,
                edit_endpoint=None,
                delete_endpoint="mosque_bp.delete_garant",
                view_endpoint="mosque_bp.PrintForm",
                list_endpoint="mosque_bp.list_garants",
                columns=['الرقم', 'اسم الكفيل', 'لقب الكفيل', 'مبلغ منحة التمدرس', 'ت. الميلاد']
            )
    return render_template('mosque/list_garants.html', results=data, form=form)


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
            database.session.add(_user)
            database.session.commit()

            mosque.user_account = _user.id
            database.session.add(mosque)
            database.session.commit()
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
            database.session.add(user)
            database.session.commit()
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
