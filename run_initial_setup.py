import json
import secrets

from werkzeug.security import generate_password_hash

from app_racine import database
from app_racine.master.models import Wilaya, Critere
from app_racine.users.models import User

import os
# ajouter les wilayas
# f = open("uploads/wilaya.json")
# print("Adding all wilayas...", end="")
# twilaya = json.load(f)
# wilayas = [Wilaya(name=instance['name'], zip_code=instance['zip_code']) for instance in twilaya]
# for w in wilayas:
#     database.session.add(w)
#     database.session.commit()
# print("done")

print("adding criteria")
f = open("uploads/critere.json")
tcriteria = json.load(f)
tcriteria = [
    dict(label = v[1], category = v[2], weight=v[3]) for v in tcriteria['values']
]
criteria = [Critere(label = instance['label'], category = instance['category'], weight = instance['weight']) for instance in tcriteria]
for w in criteria:
    database.session.add(w)
    database.session.commit()
# adding the admin user
print("adding the admin...", end="")

# x = User()
#
# x.username = secrets.token_urlsafe(8)
# x.first_name = "وارم"
# x.last_name = "وليد"
# x.phone_number = "03542610"
# password = "1091EB5A6c\january___62"
# x.password = generate_password_hash(password, "sha256")
# x.role = "administrator"
# database.session.add(x)
# database.session.commit()
#
# print('done! \npassword={}, username={}'.format(password, x.username))
