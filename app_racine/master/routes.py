from flask import session, url_for, redirect, request, flash, render_template, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required
from app_racine import db
from app_racine.master import master_bp
from app_racine.mosque.models import *
from app_racine.master.models import *
from app_racine.master.forms import *
from app_racine.mosque.forms import *
from app_racine.users.models import User

import bleach
import secrets
import sqlalchemy

ALLOWED_TAGS = bleach.ALLOWED_TAGS + ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'dt', 'dd', 'table', 'tbody', 'thead',
                                      'section',
                                      'u', 'i', 'br', 'em', 'strong','p', 't']


@master_bp.before_request
def master_bp_before_request():
    try:
        if current_user.is_authenticated and current_user.role == 'administrator':
            print("admin dashboard")
        else:
            abort(403)
    except Exception as exception:
        print(f'at {datetime.utcnow()}: {str(exception)}')
        abort(403)


@master_bp.route("/admin/dashboard")
@login_required
def admin_dashboard():
    garants = Garant.query.all()
    mosques = Mosque.query.all()
    nb_donors = User.query.filter_by(role="donor")
    data = {
        'nb_garant': len(garants) if garants else 0,
        'nb_mosques': len(mosques) if mosques else 0,
        'nb_donors': len(nb_donors) if nb_donors.all() else 0
    }
    return render_template('master/admin.html', content=data)


@master_bp.route('/Mosques/<int:page>')
@login_required
def list_mosques(page):
    data = Mosque.to_collection_dict(
        query=Mosque.query,
        page=page,
        per_page=12,
        list_endpoint="master_bp.list_mosques",
        edit_endpoint=None,
        delete_endpoint=None,
        view_endpoint=None,
        columns=['الرقم', 'الاسـم', 'العنوان', 'الصنف', 'اسم المستخدم']
    )
    return render_template('master/list_mosque.html', results=data)


@master_bp.route("/admin/Mosques/register", methods=['GET', 'POST'])
@login_required
def register_m():
    form = MosqueForm()
    form.state.choices = [('None', 'الولاية')] + [(x.id, x.name) for x in Wilaya.query.all()]
    form.username.data = str(secrets.token_hex(8))
    if form.validate_on_submit():
        t_mosques = Mosque()
        t_mosques.nom = form.nom.data
        t_mosques.addresse = form.adresse.data
        t_mosques.num_tele = form.phone_num.data
        t_mosques.state = int(form.state.data)
        t_mosques.category = form.categorie.data
        hashed_password = generate_password_hash(form.password.data, "sha256")
        t_user = User()
        t_user.username = form.username.data
        t_user.password = hashed_password
        t_user.first_name = form.first_name.data
        t_user.last_name = form.last_name.data
        t_user.role = 'imam'
        t_user.phone_number = form.phone_num_imam.data
        t_user.email = form.email.data if form.email.data != '' else None

        db.session.add(t_user)
        db.session.commit()
        t_mosques.user_account = t_user.id
        db.session.add(t_mosques)
        db.session.commit()
        flash('لقـد تم اضافة المسجد بنجاح الرجاء الاتصال بإمام المسجد و تسليم معلومات الدخـول', 'success')
        return redirect(url_for("master_bp.register_m"))
    return render_template('master/register_mosques.html', form=form)


@master_bp.route('/admin/Criteres/<int:page>')
@login_required
def list_criteres(page):
    data = Critere.to_collection_dict(
        query=Critere.query,
        page=page,
        per_page=12,
        list_endpoint="master_bp.list_criteres",
        edit_endpoint="master_bp.edit_critere",
        delete_endpoint=None,
        view_endpoint=None,
        columns=['الرقم', 'تسميـة المعيار', 'الصنف', 'المعامــل']
    )
    if not Critere.query.all():
        flash('لا توجد معايير بعد', 'info')
    return render_template('master/list_critere.html', results=data)


@master_bp.route('/admin/Criteres/register', methods=['GET', 'POST'])
@login_required
def register_critere():
    form = CritereForm()
    form.categorie.choices = [('None', 'التصنيف')] + [('الاجتماعية', 'الاجتماعية'), ('الصحية', 'الصحية'),
                                                      ('العائلية', 'العائلية')]
    if form.validate_on_submit():
        _critere = Critere()
        _critere.label = form.label.data
        _critere.category = form.categorie.data
        _critere.weight = form.poids.data
        db.session.add(_critere)
        db.session.commit()
        flash('تمت العملية بنجاح', 'success')
        return redirect(url_for('master_bp.register_critere'))
    return render_template('master/register_critere.html', form=form)


@master_bp.route('/critere/<int:_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_critere(_id):
    critere = Critere.query.get(_id)
    if not critere:
        flash('لا يوجد هذا المعيار')
        return redirect(url_for('master_bp.list_criteres', page=1))

    form = EditCritereForm()
    form.categorie.choices = [('None', '')] + [('الاجتماعية', 'الاجتماعية'), ('الصحية', 'الصحية'),
                                               ('العائلية', 'العائلية')]
    form.categorie.data = critere.category
    if request.method == 'GET':
        form.label.data = critere.label
        form.poids.data = critere.weight
    elif form.validate_on_submit():
        _critere = Critere.query.filter_by(category=form.categorie.data).filter_by(label=form.label.data).first()
        if _critere and _critere.id != critere.id:
            flash('هذا المعيار موجود من قبل')
            return redirect('master_bp.edit_critere', _id=_id)
        critere.label = form.label.data
        critere.category = form.categorie.data
        critere.weight = form.poids.data
        db.session.add(critere)
        db.session.commit()
        flash('تمت عملية التعديل بنجاح', 'success')
        return redirect(url_for('master_bp.list_criteres', page=1))
    return render_template('master/register_critere.html', form=form)


@master_bp.route('/Projects/<int:page>')
def list_projects(page):
    data = Project.to_collection_dict(
        query=Project.query,
        page=page,
        per_page=12,
        list_endpoint="master_bp.list_projects",
        edit_endpoint="master_bp.edit_project",
        delete_endpoint=None,
        view_endpoint=None,
        columns=['الرقم', 'التسميـــة', 'الوصف', 'القيمة المقربة للمبلغ', 'المبلغ المجموع']
    )
    if not Project.query.all():
        flash(' لم يتم إضافــة أية مشاريــــع .', 'info')
    return render_template('master/list_project.html', results=data)


@master_bp.route('/admin/Projets/new', methods=['GET', 'POST'])
def register_projects():
    form = ProjectsForm()
    if form.validate_on_submit():
        t_prj = Project()
        t_prj.title = form.title.data
        cleaned_data = bleach.clean(form.Description.data, tags=ALLOWED_TAGS)
        t_prj.Description = cleaned_data
        t_prj.montant_estime = form.montant_estime.data
        db.session.add(t_prj)
        db.session.commit()
        flash('تمت العملية بنجاح', 'success')
        return redirect(url_for('master_bp.register_projects'))
    return render_template('master/register_projects.html', form=form)


@master_bp.route('/projects/<int:_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(_id):
    prj = Project.query.get(_id)
    if not prj:
        flash('لا يوجد هذا المشروع')
        return redirect(url_for('master_bp.list_project', page=1))

    form = EditProjectForm()
    if request.method == 'GET':
        form.title.data = prj.title
        form.Description.data = prj.Description
        form.montant_estime.data = prj.montant_estime
    elif form.validate_on_submit():
        prj.title = form.title.data
        cleaned_data = bleach.clean(form.Description.data, tags=ALLOWED_TAGS)
        prj.Description = cleaned_data
        prj.montant_estime = form.montant_estime.data
        db.session.add(prj)
        db.session.commit()
        flash('تمت عملية التعديل بنجاح', 'success')
        return redirect(url_for('master_bp.list_projects', page=1))
    return render_template('master/register_projects.html', form=form)


@master_bp.route('/admin/update', methods=['GET', 'POST'])
@login_required
def update_parameters():
    form = ParameterForm()
    latest_parametre = ParameterUtils.query.first()
    if not latest_parametre:
        latest_parametre = ParameterUtils()
    if form.validate_on_submit():
        latest_parametre.taux_scolaire = form.taux_scolaire.data
        latest_parametre.taux_prime_m = form.taux_prime_m.data
        latest_parametre.salaire_base = form.salaire_base.data
        db.session.add(latest_parametre)
        db.session.commit()
        flash("تمت العملية بنجـــاح", "success")
        return redirect(url_for('master_bp.update_parameters'))
    elif request.method == "GET":
        form.taux_prime_m.data = latest_parametre.taux_prime_m or 0
        form.taux_scolaire.data = latest_parametre.taux_scolaire or 0
        form.salaire_base.data = latest_parametre.salaire_base or 20000
        return render_template('master/update_parametres.html', form=form)
