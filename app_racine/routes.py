from datetime import datetime
import arabic_reshaper as reshaper
from bidi import algorithm as algo
from flask_wtf import FlaskForm
from flask import render_template, redirect, flash, session, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app_racine import app, bcrypt, db
from app_racine.models import Personne, situation_garant,situation_personne
from app_racine.models import Mosque, Donneur, User, Projet, Fournit, Garant, Critere
from app_racine.models import parametre_utils
from app_racine.forms  import ProjectsForm,  RegisterGarantForm,register_new_donnation
from app_racine.forms  import LoginForms, RequestResetForm,ResetPasswordForm,FormField,personnes_par_garant
from app_racine.forms  import TokenForm, mosqueForm, donneurForm, critereForm,update_account_form
from app_racine.forms import parameter_utils_form
from app_racine.utils  import get_data_from_request,verify_presence,count_points

@app.route('/mosque/form/<string:arg>')
def print_form(arg):
   garant = Garant.query.filter_by(id = arg).first()
   if garant:
      return garant.print_form()
   return "not Found"

@app.route("/mosque/table")
def print_table():
   temp = Mosque.query.filter_by(user_account = session['user_id']).first()
   if temp:
      return temp.print_resume()
   return "not found"

@app.route("/")
@app.route("/accueil")
def accueil():
   return render_template('index.html', today = datetime.now().date())

@app.route("/admin/<string:arg>")
@login_required
def admin(arg):
    global contents
    contents = {
        'Mosques': {
                        'data' : Mosque.query.all(),
                        'template':'c_mosques.html'
        },
        'Donneurs': {
                        'data' : Donneur.query.all(),
                        'template' :'c_donneurs.html'
        },
        'Projets': {
                        'data' : Projet.query.all(),
                        'template' : 'c_projects.html'
        },
        'Criteres': {
                        'data' : Critere.query.all(),
                        'template' : 'c_criteres.html'
        }
   }
    if arg == 'home':
        return render_template('admin.html' , today = datetime.now().date() , content = contents)
    return render_template("{page}".format(page = contents[arg]['template']) ,
                           today = datetime.now().date()
                        )

@app.route('/admin/Mosques/listing')
@login_required
def list_mosques():
   content = {
               'data': [x for x in contents['Mosques']['data']],
               'columns': ['الرقم','الاسـم','الامام','العنوان','الولايــة']
           }
   return render_template('list_m.html', content = content)      

@app.route('/admin/Donneurs/listing')
@login_required
def list_donneurs():
    operations = {
                'data': [x for x in contents['Donneurs']['data']],
                'columns': ['الرقم','اللقـــب','الاســـم','العنوان','رقم الهاتف']
            }
    return render_template('list_D.html', content = operations)

@app.route('/admin/Criteres/listing')
@login_required
def list_criteres():
    content = {
                'data': [x for x in contents['Criteres']['data']],
                'columns': ['الاســــم','التصنيف','النقط']
            }
    return render_template('list_C.html', content = content)

@app.route('/admin/Projets/listing')
def list_projects():
   content= {
           'data': [x for x in contents['Projets']['data']],
           'columns': ['الرــقم','القيمة المقدرة','المبلغ الحالي','حول المشروع'] 
   }
   return render_template('list_P.html', content= content)

@app.route("/mosque/<int:arg>")
@login_required 
def mosque(arg):
    mosque_content = Mosque.query.filter_by( id = arg).first()
    return render_template('mosque.html', mosque_name = mosque_content.nom, content = mosque_content)

@app.route("/mosque/listing")
def list_garants():
    member = Mosque.query.filter_by(user_account = session['user_id']).first()
    member.tendance()
    g_list = Garant.query.filter_by(mosque_id = member.id)
    for person in g_list:
       person.get_total_sum()
    g_content = {
        'id': member.id,
        'name': member.nom,
        'data': [x for x in member.inscrits],
        'columns': ['ح.ب.ج','اســـم الكفيل','لقب الكفيل','ت. الميلاد','المبلـــغ','معلومات حول']
    }
    return render_template('list_garants.html', content = g_content)

@app.route("/donneur")
@login_required
def donneur():
   content = {
       'donneur': Donneur.query.all(),
       'operations': Fournit.query.all()
   }
   return render_template('donneur.html',contents = content, title="زكـاة : متبرع")

@app.route("/login", methods=['GET', 'POST'])
def login():
   if current_user.is_authenticated:
      m = Mosque.query.filter_by(user_account=session['user_id']).first()     
      if m :
         return redirect(url_for('mosque', arg = int(m.id)))
      elif Donneur.query.filter_by(user_account = int(session['user_id'])).first():
         return redirect(url_for('donneur'))
      else:
         return redirect(url_for('admin' , arg = 'home'))
   form = LoginForms()
   if form.validate_on_submit():
      user = User.query.filter_by(username = form.username.data).first()
      if user and bcrypt.check_password_hash(user.password, form.password.data):
         login_user(user, remember=False)
         session["user_id"] = user.id
         next_page = request.args.get('next')
         t_mosque = Mosque.query.filter_by(user_account = user.id).first()
         if  t_mosque:
            return redirect(next_page) if next_page else redirect(url_for('mosque', arg = t_mosque.id))
         elif Donneur.query.filter_by(user_account = user.id).first():
            return redirect(next_page) if next_page else redirect(url_for('donneur'))
         return redirect(next_page) if next_page  else redirect(url_for('admin' , arg='home'))
      else:
          flash('خطأ في المعلومات يرجى التأكد و إعادة المحاولة', 'danger')
   return render_template('login.html', title = "زكاة : تسجيل الدخول", form = form)

@app.route("/logout")
def logout():
   logout_user()
   return redirect(url_for("accueil"))

@app.route('/request_token', methods=['GET', 'POST'])
def request_token():
   form = RequestResetForm()
   if form.validate_on_submit():
      #user = User.query.filter_by(username = form.username.data).first()
      #send_request_token(user)
      return redirect('verify_token')
   return render_template('request_token.html', title  = "استعادة كلمة المرور", form = form)

@app.route("/verify_token", methods=['GET', 'POST'])#E/S
def verify_token():
   form = TokenForm()
   if form.validate_on_submit():
      return redirect('reset_password')
   return render_template('verify_token.html', title="استعادة كلمة المرور", form = form)

@app.route("/reset_password", methods=['GET', 'POST'])#E/S
def reset_password():
   form = ResetPasswordForm()
   pass
   return render_template('reset_password.html', title ="تغيير كلمة المرور", form = form)

@app.route("/admin/Mosques/register", methods=['GET', 'POST'])
@login_required
def register_m():
   form = mosqueForm()
   if form.validate_on_submit():
      if verify_presence(form.nom.data, form.phone_num.data, form.imam.data, form.state.data):
          flash('خطـــأ', 'danger')
          return redirect(url_for('admin', arg='Mosques'))
      t_mosques = Mosque(
                     nom = form.nom.data,
                     imam = form.imam.data,
                     addresse = form.adresse.data,
                     num_tele = form.phone_num.data,
                     state = form.state.data
                  )
      hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
      t_user = User(
                  username = form.phone_num.data,
                  password = hashed_password
              )
      db.session.add(t_user)
      db.session.commit()
      t_mosques.user_account = User.query.filter_by(username = form.phone_num.data).first().id
      db.session.add(t_mosques)
      db.session.commit()
      flash('لقـد تم اضافة المسجد بنجاح الرجاء الاتصال بإمام المسجد و تسليم معلومات الدخـول', 'success')
      return redirect(url_for('admin', arg='Mosques'))
   return render_template('register_m.html' , form_m = form)

@app.route("/admin/Donneurs/register", methods=['GET', 'POST'])
@login_required
def register_donneurs():
    form = donneurForm()
    if form.validate_on_submit():
        compte = Donneur.query.filter_by(nom = form.nom.data).first()
        if compte and (compte.prenom == form.prenom.data) and (compte.num_tele == form.num_tele.data):
            flash("هذا الشخص موجود يرجى التحقق من المعلومات و إعادة المحاولة", "danger")
            return redirect(url_for('admin', arg='Donneurs'))
        t_donneur = Donneur(
                    nom = form.nom.data,
                    prenom = form.prenom.data, 
                    adresse = form.adresse.data,
                    num_tele = form.num_tele.data,
                    )
        t_user = User(
                    username = form.num_tele.data,
                    password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                )
        db.session.add(t_user)
        db.session.commit()
        t_donneur.user_account = User.query.filter_by(unomsername = form.num_tele.data).first().id
        db.session.add(t_donneur)
        db.session.commit()
        flash('لقـد تمت الإضـــافـة بنجاح', 'success')
        return redirect(url_for('admin', arg = 'Donneurs'))
    return render_template('register_D.html', form_m = form)

@app.route('/admin/Criteres/register', methods=['GET', 'POST'])
@login_required
def register_critere():
    form = critereForm()
    if form.validate_on_submit():
        _critere = Critere(
            id = form.label.data,
            categorie = form.categorie.data,
            poids = form.poids.data
        )
        db.session.add(_critere)
        db.session.commit()
        flash('تمت العملية بنجاح', 'success')
        return redirect(url_for('admin', arg='Criteres'))
    return render_template('register_C.html', form_m = form)

@app.route('/admin/Projets/register', methods=['GET', 'POST'])
def register_projets():
    form = ProjectsForm()
    if form.validate_on_submit():
        t_prj = Projet(
              title = form.title.data,
                Description = form.Description.data,
                montant_estime = form.montant_estime.data
            )
        db.session.add(t_prj)
        db.session.commit()
        flash('تمت العملية بنجاح', 'success')
        return redirect(url_for('admin', arg='Projets'))
    return render_template('register_P.html', form_m = form)

@app.route('/mosque/register', methods=['GET', 'POST'])
@login_required
def register_garants():
    print("session id = {}".format(int(session['user_id'])))
    form = RegisterGarantForm()
    form.famille = [personnes_par_garant()]
    membre = Mosque.query.filter_by(user_account = session['user_id']).first()
    if form.validate_on_submit():
        garant = Garant(
            id = form.compte_ccp.data,
            cle_CCP = form.cle_ccp.data,
            nom = form.nom.data,
            prenom = form.prenom.data,
            date_nais = form.date_nais.data,
            num_extrait_nais = form.num_extrait_nais.data,
            mosque_id = membre.id
            )
        
        liste = request.form.getlist('situation_sante')+request.form.getlist('situation_sociale')
        db.session.add(garant)
        db.session.commit()
        for case in liste:
            status = situation_garant(
                garant_id = garant.id,
                critere_id = case
                )
            db.session.add(status)
            db.session.commit()
        personne = Personne(nom = form.famille[0].p_nom.data,
                            prenom=form.famille[0].p_prenom.data,
                            date_naissance = form.famille[0].p_date_nais.data,
                            relation_ship= form.famille[0].p_relation_ship.data,
                            garant_id = garant.id)
        db.session.add(personne)
        db.session.commit()
        if form.famille[0].handicap.data:
          handicap = situation_personne(personne_id = personne.id,critere_id = "اعاقة")
          db.session.add(handicap)
          db.session.commit()

        if form.famille[0].education.data:
          education = situation_personne(personne_id = personne.id,critere_id = "فرد متمدرس")
          db.session.add(education)
          db.session.commit()

        if form.famille[0].malade_cronic.data:
          malade_cronic = situation_personne(personne_id = personne.id,critere_id = "مرض مزمن")
          db.session.add(malade_cronic)
          db.session.commit()
        
        get_data_from_request(request,garant.id)
        form.famille = Personne.query.filter_by(garant_id = garant.id)
        count_points(garant,form.famille)
        db.session.add(garant)
        db.session.commit()
        membre.tendance()
        flash("لقد تم اضـــــافة الفرد بنجاح","success")
        return redirect(url_for('register_garants'))
    return render_template('register_G.html',content = membre, form_m = form)

@app.route("/mosque/Donnations/register",methods=['GET','POST'])
@login_required
def register_donnation():
   form = register_new_donnation()
   membre = Mosque.query.filter_by(user_account = session['user_id']).first()
   if form.validate_on_submit():
      operation = Fournit(
         mosque_id = int(membre.id),
         donneur_id= int(form.donneur.data),
         montant = form.montant.data,
         date = datetime.today()
      )
      db.session.add(operation)
      db.session.commit()
      flash("تمت الاضافـــة بنجاح", "success")
      return redirect(url_for('register_donnation'))
   return render_template("register_don.html",content = membre,form_m= form)

@app.route("/mosque/Donnations")
@login_required
def list_dons():
   mosque = Mosque.query.filter_by(user_account = session['user_id']).first()
   temp1 = Fournit.query.filter_by(mosque_id = mosque.id).all()
   operations = []
   for operation in temp1:
      temp= Donneur.query.filter_by(id=operation.donneur_id).first()
      person = {
               "nom": temp.nom,
               "prenom": temp.prenom
            }
      operations.append((operation, person))
      del person

   donnations= {
           'data': operations,
           'columns': ['الرقـم','الاسم و اللقب','القيمــة','التاريخ']
         }
   return render_template('list_dons.html', donnations= donnations, content=mosque)

@app.route("/mosque/Update/<int:arg>", methods=['GET','POST'])
@login_required
def update_info(arg):
   mosque = Mosque.query.get(int(arg))
   form = update_account_form()
   if mosque.user_account != session['user_id']:
      abort(403)
   if form.validate_on_submit():
      mosque.imam = form.nom_imam.data
      mosque.num_tele = form.num_tele.data
      db.session.add(mosque)
      db.session.commit()
      flash("تمت عملية التعديل بنجاح", "success")
      return redirect(url_for('mosque', arg=arg))
   elif request.method == 'GET':
      form.nom_imam.data = mosque.imam
      form.num_tele.data = mosque.num_tele
   return render_template('update_mosque.html',content = mosque, form_m = form)
@app.route('/admin/update', methods=['GET','POST'])
def update_parameters():
   form = parameter_utils_form()
   lastest_parametre = parametre_utils.query.all()[0]
   if form.validate_on_submit():
      lastest_parametre.taux_scolaire = int(form.taux_scolaire.data)
      lastest_parametre.taux_prime_m = int(form.taux_prime_m.data)
      db.session.add(lastest_parametre)
      db.session.commit()
      flash("تمت العملية بنجـــاح", "success")
      return redirect(url_for('admin',arg='home'))
   elif request.method =="GET":
      form.taux_prime_m.data = lastest_parametre.taux_prime_m
      form.taux_scolaire.data = lastest_parametre.taux_scolaire
      return render_template('update_parametres.html', form_m = form)