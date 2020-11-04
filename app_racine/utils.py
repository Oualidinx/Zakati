from werkzeug.exceptions import BadRequestKeyError
from flask import make_response, session
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.rl_config import TTFSearchPath
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
from bidi.algorithm import get_display
from arabic_reshaper import arabic_reshaper as reshaper
from app_racine.models import Mosque, Critere, Garant, User, parametre_utils
from app_racine.models import situation_personne, situation_garant, Personne
from app_racine import db
import os




def is_concerned_prime_s(garant_id):
    garant = Garant.query.filter_by(id=garant_id).first()
    taux_scolaire = parametre_utils.query.all()[0].taux_scolaire
    situation = []
    for person in garant.familles:
        try:
            temp = situation_personne.query.filter_by(personne_id=person.id).filter_by(
                critere_id='فرد متمدرس').first().personne_id
            situation.append(temp)
        except:
            pass
    if len(situation) > 0:
        return len(situation) * taux_scolaire
    return False


def project_status(project_id):
    pass


def is_concerned_prime_m(garant_id):
    garant = Garant.query.filter_by(id=garant_id).first()
    taux_prime_m = parametre_utils.query.all()[0].taux_prime_m
    salaire_base = parametre_utils.query.all()[0].salaire_base
    is_jobless = 'بطال' in situation_garant.query.filter_by(garant_id=garant_id)
    if is_jobless:
        return (len(garant.familles) + 1) * taux_prime_m

    if ((len(garant.familles) + 1) * taux_prime_m) < salaire_base:
        return salaire_base - ((len(garant.familles) + 1) * taux_prime_m)

    return False


def get_data_from_request(requete, garant_id):
    count = 2
    while True:
        try:
            p = Personne(
                nom=requete.form["p_{}_nom".format(str(count))],
                prenom=requete.form["p_{}_prenom".format(str(count))],
                date_naissance=requete.form["p_{}_date_nais".format(str(count))],
                relation_ship=requete.form["p_{}_relation_ship".format(str(count))],
                garant_id=garant_id
            )
            db.session.add(p)
            db.session.commit()
            if requete.form.getlist("p_{}_malade_cronic".format(str(count))):
                malade_cronic = situation_personne(critere_id="مرض مزمن", personne_id=p.id)
                db.session.add(malade_cronic)
                db.session.commit()

            if requete.form.getlist("p_{}_education".format(str(count))):
                education = situation_personne(critere_id="فرد متمدرس", personne_id=p.id)
                db.session.add(education)
                db.session.commit()

            if requete.form.getlist("p_{}_handicap".format(str(count))):
                handicap = situation_personne(critere_id="اعاقة", personne_id=p.id)
                db.session.add(handicap)
                db.session.commit()
        except BadRequestKeyError as e:
            break
        count = count + 1


def verify_presence(data1, data2, data3, data4):
    m = Mosque.query.filter_by(nom=data1).first()
    m1 = Mosque.query.filter_by(num_tele=data2).first()
    if m and (m.state == data4):
        return True
    if m1 and m1.imam == data3:
        return True
    return False


def count_points_personne(person):
    status = situation_personne.query.filter_by(personne_id=person.id)
    points = 0
    for situation in status:
        poids = Critere.query.filter_by(id=situation.critere_id).first().poids
        points += poids
    return points


def count_points(garant, persons):
    S = situation_garant.query.filter_by(garant_id=garant.id)
    for situation in S:
        poids = Critere.query.filter_by(id=situation.critere_id).first().poids
        garant.Solde_points += poids
    for person in persons:
        garant.Solde_points += count_points_personne(person)


def get_reshaped_text(text):
    arabic_text = reshaper.reshape(text)
    arabic_text = get_display(arabic_text)
    return arabic_text


from io import BytesIO


# construite le formulaire
def print_PDF_view(garant_id):
    output = BytesIO()
    person = Garant.query.filter_by(id=garant_id).first()
    TTFSearchPath.append(os.path.dirname(os.path.abspath('TimesNewRoman.tff')) + '/app_racine/static/fonts')
    pdfmetrics.registerFont(TTFont("Times", 'TimesNewRoman.ttf'))
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
    p.drawRightString(530, 560, get_reshaped_text(u'الإســم :  ' + person.prenom))
    p.drawRightString(300, 560, get_reshaped_text(u'اللقــــب :  ' + person.nom))
    p.drawRightString(530, 540, get_reshaped_text(u'تاريـخ الميلاد : ' + str(person.date_nais)[:10]))
    # print("Utils-> date_nais: {}".format(str(person.date_nais)[:10]))
    # p.drawRightString(300 , 540 , get_reshaped_text(u'مكان الميلاد : '+person.lieu_nais))
    # p.drawRightString(530 , 520 , get_reshaped_text(u'العنوان : '+person.Adress))
    p.setFontSize(17)
    """p.drawRightString(550 , 490 , get_reshaped_text(u'2- الحالة الاجتماعية :'))
    p.setFontSize(16)
    p.drawRightString(530 , 470 , get_reshaped_text(u'الحالة المدنيــة : ' + person.sit_famille))
    p.setFontSize(17)
    p.drawRightString(550 , 445 , get_reshaped_text(u'3- الســكن : '))
    p.setFontSize(16)
    p.drawRightString(480 , 445 , get_reshaped_text(person.log))
    p.setFontSize(17)
    p.drawRightString(550 , 420 , get_reshaped_text(u'4- العمــــل : '))
    p.setFontSize(16)
    p.drawRightString(480 , 420  , get_reshaped_text(person.Profession))
    p.setFontSize(17)
    p.drawRightString(550 , 395 , get_reshaped_text(u'5- الاستفادة من خدمات الضمان الاجتماعـي : '))
    p.setFontSize(16)
    p.drawRightString(280, 395  , get_reshaped_text(person.Health_care))
    p.setFontSize(17)
    p.drawRightString(550 , 365 , get_reshaped_text(u'6- أفراد على نفقـة طالـب الزكاة (العدد) : '))
    p.setFontSize(16)
    p.drawRightString(500 , 335 , get_reshaped_text(u'أ- الفروع الصُّلبِيُّون : '+str(len(Personne.query.filter_by(garant_id = person.CCP , relation = "ابن")))))
    p.drawRightString(500 , 305 , get_reshaped_text(u' ب- الأصـول (الأب، الأم، الجـد، الجـدة) : '+str(len(personne.objects.filter(fk_id_garant = person.CCP , relation = "والد(ة)")))))
    p.drawRightString(500 , 275 , get_reshaped_text(u'ج- حـالات أخـرى : '+str(len(personne.objects.filter(fk_id_garant = person.CCP , relation = "اخرى")))))
    """
    p.drawRightString(550, 200, get_reshaped_text(u'في : برج بو عريريج'))
    p.drawRightString(400, 200, get_reshaped_text(u'التــــاريخ : ' + str(datetime.today())[:10]))
    p.drawRightString(200, 200, get_reshaped_text(u'إمضـاء المعنـي : '))
    p.setFontSize(17)
    p.drawCentredString(320, 100, get_reshaped_text(u'أقسـم بالله العظيم أن كل المعلومات التي قدمتها أعلاه صحيحة'))
    p.save()
    pdf_out = output.getvalue()
    output.close()
    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = 'inline; filename="{id}.pdf"'.format(id=person.id)
    print("Utils: attachment; filename=\"{id}.pdf\"".format(id=person.id))
    response.mimetype = 'application/pdf'
    return response


# la liste finale
def printPDF_resume_view():
    member = Mosque.query.filter_by(user_account=session['user_id']).first()
    garant_list = list(Garant.query.filter_by(mosque_id=member.id))
    TTFSearchPath.append(os.path.dirname(os.path.abspath('TimesNewRoman.tff'))+'/app_racine/static/fonts')
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
    canv.drawRightString(800, 510, get_reshaped_text(u'البلديــة :' + member.state))
    canv.drawRightString(800, 488, get_reshaped_text(u'التاريــخ : ' + str(datetime.today())[:10]))
    # les données
    data = [(get_reshaped_text(u'      الإمضـاء      '), get_reshaped_text(u'        بطاقة الهوية      '),
             get_reshaped_text(u'\t\t القيمة (د.ج)\t\t'), get_reshaped_text(u'\tعدد الاسهم\t'),
             get_reshaped_text(u'\t تاريخ الميلاد \t '), get_reshaped_text(u'          الاســم و اللقــب          '),
             get_reshaped_text(u'الرقم'))]
    count = 1

    nb_pages = 1

    if (len(garant_list) > 15):
        nb_pages = nb_pages + int((len(garant_list) - 15) / 18)
        if ((len(garant_list) - 15) % 18 != 0):
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
                "", "", person.Solde_part_financiere, person.Solde_finale,
                get_reshaped_text(str(person.date_nais)[:10]), \
                get_reshaped_text(person.nom) + "    " + get_reshaped_text(person.prenom), count)
            montant = montant + person.Solde_finale
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
    response.headers['Content-Disposition'] = 'inline; filename=' + str(datetime.today())[:10] + '.pdf'
    response.mimetype = "application/pdf"
    return response
