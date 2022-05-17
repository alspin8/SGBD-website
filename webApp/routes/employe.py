from db.src.requests import lire_employes, lire_all, shortuuid, insert_employe, insert_travailler, update_employe, delete_employe, lire_employe, update_travailler, lire_employe_full
from db.src.dataHandle import concat_employes, convert_employe_service_in_list
from flask import Blueprint, render_template, request, redirect, url_for, flash

employe = Blueprint('employe', __name__)

@employe.route('/')
def index():
    employes = lire_employes()
    employes = concat_employes(employes)
    return render_template("employe.index.html", employes=employes)

@employe.route('/add', methods=["GET", "POST"])
def add():
    
    if request.method == "GET":
        services = lire_all("Service")
        communes = lire_all("Commune")
        return render_template("employe.form.html", services=services, communes=communes)
        
    elif request.method == "POST":
        new_employe = request.form.to_dict()
        employes = lire_employes()
        if len([1 for employe in employes if employe[1] == new_employe['nom'] and employe[2] == new_employe['prenom'] and employe[3] == new_employe['ddn']]):
            flash("Employé déjà enregistré !")
            return redirect(url_for("employe.add"))
        new_employeId = str(shortuuid.uuid()[:12])
        # if insert_travailler(new_employeId,new_employe['serviceId']) :
            # flask.message_flashed("Ce service est déjà assigné à cet employé")
            # return redirect(url_for("employe.add"))
        print(new_employe)
        insert_travailler(new_employeId,new_employe['serviceId'])
        insert_employe(new_employeId, new_employe)
        return redirect(url_for('employe.index'))

@employe.route('/delete/<id>')
def delete(id):
    delete_employe(id)
    return redirect(url_for('employe.index'))

@employe.route('/update/<id>', methods=["GET", "POST"])
def update(id):

    if request.method == 'GET':
        services = lire_all("Service")
        communes = lire_all("Commune")
        employe_to_update = lire_employe_full(id)
        if len(employe_to_update) > 1:
            employe_to_update = concat_employes(employe_to_update)[0]
        else:
            employe_to_update = convert_employe_service_in_list(employe_to_update)
        return render_template("employe.form.html", employe=employe_to_update, services=services, communes=communes)

    elif request.method == "POST":
        old_employe = lire_employe_full(id)
        updated_employe = request.form.to_dict()
        update_employe(id, updated_employe)
        update_travailler(old_employe, updated_employe)
        return redirect(url_for('employe.index'))