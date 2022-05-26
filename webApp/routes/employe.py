from db.src.requests import lire_employes, lire_all, shortuuid, insert_employe, insert_travailler, update_employe, delete_employe, lire_employe, update_travailler, lire_travailler_by_employeId, lire_employe_services
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
            if len([1 for employe in employes if employe[1].upper() == new_employe['nom'].upper() and employe[2].upper() == new_employe['prenom'].upper() and employe[3] == new_employe['ddn']]):
                flash("Employé déjà enregistré !")
                return redirect(url_for("employe.add"))
            new_employeId = str(shortuuid.uuid()[:12])
            for serviceId in new_employe['serviceIds']:
                insert_travailler(new_employeId, serviceId)
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
        employe_to_update = lire_employe(id)
        employe_to_update += ([service_id[1] for service_id in lire_travailler_by_employeId(id)],)
        print(employe_to_update)
        return render_template("employe.form.html", employe=employe_to_update, services=services, communes=communes)

    elif request.method == "POST":
        old_employe_travaillers = lire_employe_services(id)
        old_employe_services = [old_employe_travailler[1] for old_employe_travailler in old_employe_travaillers]
            
        updated_employe = request.form.to_dict()
        updated_employe_services = [int(service) for service in updated_employe["serviceIds"] if service != ","]
        
        travailler_to_add = [service for service in updated_employe_services if service not in old_employe_services]
        travailler_to_del = [service for service in old_employe_services if service not in updated_employe_services]
        
        update_employe(id, updated_employe)
        update_travailler(id, travailler_to_add, travailler_to_del)
        return redirect(url_for('employe.index'))