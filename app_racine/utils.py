from werkzeug.exceptions import BadRequestKeyError
from flask import make_response, session
from flask_login import current_user
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.rl_config import TTFSearchPath
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors

from bidi.algorithm import get_display

from arabic_reshaper import arabic_reshaper

from app_racine.mosque.models import Garant, GarantProject, SituationGarant, Mosque, Personne, SituationPerson
from app_racine.master.models import *
from app_racine import db

import os
from io import BytesIO

from datetime import datetime


def is_concerned_prime_s(garant_id):
    garant = Garant.query.filter_by(id=garant_id).first()
    taux_scolaire = ParameterUtils.query.first().taux_scolaire
    situation = []
    if Critere.query.all():
        for person in garant.familles:
            temp = SituationPerson.query.filter_by(personne_id=person.id) \
                                        .filter_by(critere_id=Critere.query.filter_by(label='فرد متمدرس') \
                                                   .first().id) \
                                        .first().personne_id
            if temp:
                situation.append(temp)

        if len(situation) > 0:
            garant.prime_scolaire = len(situation) * taux_scolaire
            db.session.add(garant)
            db.session.commit()
            return len(situation) * taux_scolaire
    return None


def is_concerned_prime_m(garant_id):
    garant = Garant.query.filter_by(id=garant_id).first()
    taux_prime_m = ParameterUtils.query.first().taux_prime_m
    salaire_base = ParameterUtils.query.first().salaire_base
    is_jobless = Critere.query.join(SituationGarant, SituationGarant.critere_id == Critere.id) \
        .filter(Critere.label == 'بطال').first()
    if is_jobless:
        garant.prime_mensuelle = (len(garant.familles) + 1) * taux_prime_m
        db.session.add(garant)
        db.session.commit()
        return (len(garant.familles) + 1) * taux_prime_m

    if ((len(garant.familles) + 1) * taux_prime_m) < salaire_base:
        garant.prime_mensuelle = salaire_base - ((len(garant.familles) + 1) * taux_prime_m)
        db.session.add(garant)
        db.session.commit()
        return salaire_base - ((len(garant.familles) + 1) * taux_prime_m)
    return None


def get_data_from_request(requete, garant_id):
    count = 2
    max_clicks = requete.form.get('max_clicks')
    if Critere.query.all():
        for i in range(count, int(max_clicks) + 1):
            if f'p_{i}_nom' not in dict(requete.form):
                continue
            else:
                _person = Garant.query.filter_by(nom=requete.form[f"p_{i}_nom"]) \
                    .filter_by(prenom=requete.form[f"p_{i}_prenom"]) \
                    .filter_by(date_nais=datetime.strptime(requete.form[f"p_{i}_date_nais"], '%Y-%m-%d')) \
                    .first()
                if _person:
                    return False
                p = Personne()
                p.nom = requete.form[f"p_{i}_nom"]
                p.prenom = requete.form[f"p_{i}_prenom"]
                p.date_naissance = datetime.strptime(dict(requete.form)[f"p_{i}_date_nais"], '%Y-%m-%d')
                p.relation_ship = requete.form[f"p_{i}_relation_ship"]
                p.garant_id = garant_id
                db.session.add(p)
                db.session.commit()
                if requete.form.get(f"p_{i}_malade_cronic") == "y" and Critere.query.filter_by(
                        label="مرض مزمن").first():
                    malade_cronic = SituationPerson()
                    malade_cronic.critere_id = Critere.query.filter_by(label="مرض مزمن").first().id
                    malade_cronic.personne_id = p.id
                    db.session.add(malade_cronic)
                    db.session.commit()

                if requete.form.get(f"p_{i}_education") == 'y' and Critere.query.filter_by(
                        label="فرد متمدرس").first():
                    education = SituationPerson()
                    education.critere_id = Critere.query.filter_by(label="فرد متمدرس").first().id
                    education.personne_id = p.id
                    db.session.add(education)
                    db.session.commit()
                if requete.form.get(f"p_{i}_handicap") == 'y' and Critere.query.filter_by(
                        label="اعاقة").first():
                    handicap = SituationPerson()
                    handicap.critere_id = Critere.query.filter_by(label="اعاقة").first().id
                    handicap.personne_id = p.id
                    db.session.add(handicap)
                    db.session.commit()
        return True
    return False


def verify_presence(data1, data2, data3, data4):
    m = Mosque.query.filter_by(nom=data1).first()
    m1 = Mosque.query.filter_by(num_tele=data2).first()
    if m and (m.state == data4):
        return True
    if m1 and m1.imam == data3:
        return True
    return False


def count_points_person(person):
    status = SituationPerson.query.filter_by(personne_id=person.id).all()
    if status:
        points = 0
        for situation in status:
            w = Critere.query.filter_by(id=situation.critere_id).first()
            if w:
                weight = w.weight
                points += weight
        return points
    return 0


def count_points(garant, persons):
    status = SituationGarant.query.filter_by(garant_id=garant.id).all()
    if status:
        for situation in status:
            weight = Critere.query.filter_by(id=situation.critere_id).first().weight
            garant.Solde_points += weight
        for person in persons:
            garant.Solde_points += count_points_person(person)


def get_reshaped_text(text):
    arabic_text = arabic_reshaper.reshape(text)
    arabic_text = get_display(arabic_text)
    return arabic_text


# construite le formulaire
def PrintPDFView(garant_id):
    output = BytesIO()
    garant = Garant.query.get(garant_id)
    persons = Personne.query.filter_by(garant_id=garant.id).all()
    resume = dict()
    resume['enfants'] = len([p for p in persons if p.relation_ship == "ابن(ة)"])
    query = Personne.query.join(SituationPerson, Personne.id == SituationPerson.personne_id).add_columns(
        Personne.id, Personne.garant_id, SituationPerson.critere_id)
    result = query.filter_by(critere_id='فرد متمدرس')
    result_students = result.filter(Personne.garant_id == garant.id)
    resume['students'] = len(result_students.all())
    result_origins = set(query.filter(Personne.garant_id == garant.id).all()) - set(result_students.all())
    resume['origins'] = len([p for p in result_origins if p.critere_id != 'زوجة'])
    del query
    query = Critere.query.join(SituationGarant, Critere.id == SituationGarant.critere_id) \
        .add_columns(Critere.id, Critere.category).filter(SituationGarant.garant_id == garant.id)
    resume['status_soc'] = query.filter(Critere.category == 'الاجتماعية').all()
    resume['status_sante'] = query.filter(Critere.category == 'الصحية').all()
    resume['status_fam'] = query.filter(Critere.category == 'العائلية').all()
    TTFSearchPath.append(os.path.dirname(os.path.abspath('Times_New_Roman.tff')) + '/app_racine/static/fonts')
    pdfmetrics.registerFont(TTFont("Times", 'Times_New_Roman.ttf'))
    member = Mosque.query.filter_by(user_account=session['user_id']).first()
    p = canvas.Canvas(output, pagesize=A4)
    p.setPageSize(A4)
    p.setFont('Times', 20)
    p.drawCentredString(300, 800, get_reshaped_text(u'الجمهورية الجزائرية الديمقراطية الشعبية'))
    p.drawCentredString(300, 780, get_reshaped_text(u'وزارة الشؤون الدينية و الأوقاف'))
    p.setFontSize(30)
    p.drawCentredString(300, 720, get_reshaped_text(u'صنـدوق الزكـاة'))
    p.setFont("Times", 16)
    p.drawRightString(550, 690, get_reshaped_text(u'مديرية الشؤون الدينية لولاية برج بو عريريج'))
    p.drawRightString(550, 665, get_reshaped_text(u' مسجد :' + member.nom))
    p.setFontSize(22)
    p.drawCentredString(300, 630, get_reshaped_text(u'إستمـارة طلـب الزكـاة'))
    p.setFontSize(17)
    p.drawRightString(550, 580, get_reshaped_text(u'1- التعريــف :'))
    p.setFontSize(16)
    p.drawRightString(530, 560, get_reshaped_text(u'الإســم :  ' + garant.prenom))
    p.drawRightString(300, 560, get_reshaped_text(u'اللقــــب :  ' + garant.nom))
    p.drawRightString(530, 540, get_reshaped_text(u'تاريـخ الميلاد : ' + str(garant.date_nais)[:10]))
    p.drawRightString(300, 540, get_reshaped_text(u'مكان الميلاد : '))
    p.drawRightString(530, 520, get_reshaped_text(u'العنوان : '))
    p.setFontSize(17)
    p.drawRightString(550, 490, get_reshaped_text(u'2- الحالة الاجتماعية :'))
    p.setFontSize(14)
    w, h = 530, 470
    for x in resume['status_soc']:
        p.drawRightString(w, h, str(x.id))  # get_reshaped_text(str(x.id))
        h = h - 20
    p.setFontSize(17)
    p.drawRightString(550, h, get_reshaped_text(u'3- الحالة الصحيــــة :'))
    p.setFontSize(14)
    h = h - 20
    for status in resume['status_sante']:
        p.drawRightString(530, h, get_reshaped_text(status.id))
        h = h - 20
    p.setFontSize(17)
    p.drawRightString(550, h, get_reshaped_text(u'6- أفراد على نفقـة طالـب الزكاة (العدد) : '))
    p.setFontSize(16)
    h = h - 30
    p.drawRightString(500, h, get_reshaped_text(
        u'أ- الفروع الصُّلبِيُّون : ' + str(resume['enfants'])))
    h = h - 30
    p.drawRightString(500, h,
                      get_reshaped_text(u' ب- الأصـول (الأب، الأم، الجـد، الجـدة) : ' + str(resume['origins'])))
    h = h - 30
    """p.drawRightString(500, 275, get_reshaped_text(
        u'ج- حـالات أخـرى : ' + str(len(Personne.objects.filter(fk_id_garant=garant.id, relation="اخرى")))))"""
    p.drawRightString(550, h, get_reshaped_text(u'في : برج بو عريريج'))
    p.drawRightString(400, h, get_reshaped_text(u'التــــاريخ : ' + str(datetime.today())[:10]))
    p.drawRightString(200, h, get_reshaped_text(u'إمضـاء المعنـي : '))
    p.setFontSize(17)

    p.drawCentredString(320, 100, get_reshaped_text(u'أقسـم بالله العظيم أن كل المعلومات التي قدمتها أعلاه صحيحة'))
    p.save()
    pdf_out = output.getvalue()
    output.close()
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = f'inline; filename="{garant.first_name} \
                                                {garant.last_name} {str(datetime.utcnow().date())}.pdf" '

    response.mimetype = 'application/pdf'
    return response


# la liste finale
def PrintPDFResumeView(project_id):
    member = Mosque.query.filter_by(user_account=session['user_id']).first()

    TTFSearchPath.append(os.path.dirname(os.path.abspath('Times_New_Roman.tff')) + '/app_racine/static/fonts')
    styles = getSampleStyleSheet()
    style = styles["BodyText"]
    pdfmetrics.registerFont(TTFont("Times", 'Times_New_Roman.ttf'))
    style.font = "Times"
    output = BytesIO()
    canv = canvas.Canvas(output, pagesize=landscape(A4))
    canv.setPageSize(landscape(A4))
    canv.setFont("Times", 22)
    canv.drawCentredString(400, 550, get_reshaped_text(u'قائمـة المستفيديــن'))
    canv.setFontSize(18)
    canv.drawCentredString(400, 528, get_reshaped_text(u'مســجد ' + member.nom))
    canv.setFontSize(16)
    canv.drawRightString(800, 510, get_reshaped_text(u'الولايـــة :' + Wilaya.query.get(member.state).name))
    canv.drawRightString(800, 488, get_reshaped_text(u'التاريــخ : ' + str(datetime.utcnow().date())))
    garant_list = Garant.query.filter_by(mosque_id=member.id).filter_by(is_active=1).all()
    project = Project.query.get(project_id)
    data = [(get_reshaped_text(u'      الإمضـاء      '), get_reshaped_text(u'        بطاقة الهوية      '),
             get_reshaped_text(u'\t\t القيمة (د.ج)\t\t'), get_reshaped_text(u'\tعدد الاسهم\t'),
             get_reshaped_text(u'\t تاريخ الميلاد \t '), get_reshaped_text(u'          الاســم و اللقــب          '),
             get_reshaped_text(u'الرقم'))]
    if project and project.title == 'المنحة الشهرية':
        canv.setFont("Times", 22)
        canv.drawCentredString(400, 550, get_reshaped_text(u'قائمـة المستفيديــن من المنحة الشهرية'))
        garant_list = Garant.query.join(Mosque, Mosque.id == Garant.mosque_id) \
            .filter(Mosque.usser_account == current_user.id) \
            .filter(is_concerned_prime_m(Garant.id) is not None)
    elif project and project.title == 'منحة التمدرس':
        canv.setFont("Times", 22)
        canv.drawCentredString(400, 550, get_reshaped_text(u'قائمـة المستفيديــن من منحة التمدرس'))
        garant_list = Garant.query.join(Mosque, Mosque.id == Garant.mosque_id) \
            .filter(Mosque.usser_account == current_user.id) \
            .filter(is_concerned_prime_s(Garant.id) is not None)
    # les données

    count = 1

    nb_pages = 1

    if len(garant_list) > 15:
        nb_pages = nb_pages + int((len(garant_list) - 15) / 18)
        if (len(garant_list) - 15) % 18 != 0:
            nb_pages = nb_pages + 1
    i = 1

    debut, fin = 0, 0
    montant = 0
    while i <= nb_pages:
        data = [(get_reshaped_text(u'      الإمضـاء      '), get_reshaped_text(u'        بطاقة الهوية        '),
                 get_reshaped_text(u'        القيمة (د.ج)        '), get_reshaped_text(u'    عدد الاسهم    '),
                 get_reshaped_text(u'    تاريخ الميلاد    '),
                 get_reshaped_text(u'            الاســم و اللقــب            '), get_reshaped_text(u'الرقم'))]
        if i == 1:
            if len(garant_list) < 15:
                debut, fin = 0, len(garant_list)
            else:
                debut, fin = 0, 15
        else:
            if i == nb_pages and ((len(garant_list) - 15) % 18 != 0):
                debut, fin = fin, fin + (len(garant_list) - 15) % 18
            else:
                debut, fin = fin, fin + 18
        donnee = garant_list[debut: fin]

        for person in donnee:
            temp = (
                "", "", person.get_total_sum(), person.Solde_finale,
                get_reshaped_text(str(person.date_nais.date())),
                get_reshaped_text(person.nom) + "    " + get_reshaped_text(person.prenom), count)
            montant = montant + person.Solde_finale
            if project and project.title == 'المنحة الشهرية':
                temp = (
                    "", "", person.get_total_sum(), person.prime_mensuelle,
                    get_reshaped_text(str(person.date_nais.date())),
                    get_reshaped_text(person.nom) + "    " + get_reshaped_text(person.prenom), count)
                montant = montant + person.prime_mensuelle
            elif project and project.title == 'منحة التمدرس':
                temp = (
                    "", "", person.get_total_sum(), person.prime_scolaire,
                    get_reshaped_text(str(person.date_nais.date())),
                    get_reshaped_text(person.nom) + "    " + get_reshaped_text(person.prenom), count)
                montant = montant + person.prime_scolaire
            data.append(temp)
            count = count + 1

        t = Table(data, rowHeights=25)
        t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), "Times"),
                               ('FONTSIZE', (0, 0), (-1, -1), 14),
                               ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        if i == 1:
            aW, aH = 600, 480
        else:
            aW, aH = 600, 550
        w, h = t.wrap(aW, aH)
        t.drawOn(canv, 70, aH - h)
        canv.setFont("Times", 15)
        canv.drawCentredString(400, 30, str(i))
        i = i + 1
        data = []
        canv.showPage()

    canv.save()
    pdf_out = output.getvalue()
    output.close()
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = 'inline; filename=' + member.nom+"_"+str(datetime.today())[:10] + '.pdf'
    response.mimetype = "application/pdf"
    return response
