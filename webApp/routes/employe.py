from click import command
from db.dataBase import *
from flask import Blueprint, render_template, request, redirect, url_for

employe = Blueprint('employe', __name__)
table = "Employe"

@employe.route('/')
def index():
    employes = lire_employe()
    return render_template("employe.index.html", employes=employes)

@employe.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "GET":
        services = lire_all("Service")
        communes = lire_all("Commune")
        return render_template("employe.form.html", services=services, communes=communes)
    elif request.method == "POST":
        new_employe = request.form.to_dict()
        insert_employe(new_employe['communeId'], new_employe['serviceId'], new_employe['nom'], new_employe['prenom'], new_employe['ddn'], new_employe['adresse'])
        return redirect(url_for('employe.index'))

@employe.route('/delete/<id>')
def delete(id):
    delete_by_id(table, "employeId", id)
    return redirect(url_for('employe.index'))

@employe.route('/update/<id>', methods=["GET", "POST"])
def update(id):
    if request.method == 'GET':
        services = lire_all("Service")
        communes = lire_all("Commune")
        employe_to_update = lire_by_id(table, "employeId", id)
        return render_template("employe.form.html", employe=employe_to_update, services=services, communes=communes)
    elif request.method == "POST":
        updated_employe = request.form.to_dict()
        update_employe(id, updated_employe['communeId'], updated_employe['serviceId'], updated_employe['nom'], updated_employe['prenom'], updated_employe['ddn'], updated_employe['adresse'])
        return redirect(url_for('employe.index'))