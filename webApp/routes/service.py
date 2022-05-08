from db.dataBase import *
from flask import Blueprint, render_template, request, redirect, url_for

service = Blueprint('service', __name__)
table = "Service"

@service.route('/')
def index():
    services = lire_all(table)
    return render_template("service.index.html", services=services)

@service.route('/add', methods=["GET", "POST"])
def add():

    if request.method == "GET":
        return render_template("service.form.html")

    elif request.method == "POST":
        new_service = request.form.to_dict()
        insert_service(new_service['nom'])
        return redirect(url_for('service.index'))

@service.route('/delete/<id>')
def delete(id):
    delete_by_id(table, "serviceId", id)
    return redirect(url_for('service.index'))

@service.route('/update/<id>', methods=["GET", "POST"])
def update(id):

    if request.method == 'GET':
        updated_service = lire_by_id(table, "serviceId", id)
        return render_template("service.form.html", service=updated_service)
        
    elif request.method == "POST":
        updated_service = request.form.to_dict()
        update_service(id, updated_service['nom'])
        return redirect(url_for('service.index'))

