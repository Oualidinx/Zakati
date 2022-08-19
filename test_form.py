from app_racine import create_app
from app_racine.mosque.forms import UpdateFamillyForm, PersonForm
from flask import render_template


app = create_app('testing')
@app.route('/test_form', methods=['GET','POST'])
def test_form():
    form = UpdateFamillyForm()
    print("here")
    # form.entities.append_entry(PersonForm())
    return render_template('test_form.html', form = form, f_form = PersonForm())

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")
