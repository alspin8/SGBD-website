from db.src.requests import *
from flask import Blueprint, render_template, request, redirect, url_for

service = Blueprint('service', __name__)

@service.route('/')
def index():
    services = lire_services()
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
    delete_service(id)
    return redirect(url_for('service.index'))

@service.route('/update/<id>', methods=["GET", "POST"])
def update(id):

    if request.method == 'GET':
        updated_service = lire_service(id)
        print(updated_service)
        return render_template("service.form.html", service=updated_service)
        
    elif request.method == "POST":
        updated_service = request.form.to_dict()
        update_service(id, updated_service['nom'])
        return redirect(url_for('service.index'))

