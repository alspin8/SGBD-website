from db.src.requests import *
from flask import Blueprint, render_template, request, redirect, url_for

commune = Blueprint('commune', __name__)

@commune.route('/')
def index():
    communes = lire_communes()
    return render_template("commune.index.html", communes=communes)

@commune.route('/add', methods=["GET", "POST"])
def add():

    if request.method == "GET":
        return render_template("commune.form.html")

    elif request.method == "POST":
        new_commune = request.form.to_dict()
        insert_commune(new_commune['nom'], new_commune['cdp'])
        return redirect(url_for('commune.index'))

@commune.route('/delete/<id>')
def delete(id):
    delete_commune(id)
    return redirect(url_for('commune.index'))

@commune.route('/update/<id>', methods=["GET", "POST"])
def update(id):

    if request.method == 'GET':
        updated_commune = lire_commune(id)
        return render_template("commune.form.html", commune=updated_commune)
        
    elif request.method == "POST":
        updated_commune = request.form.to_dict()
        update_commune(id, updated_commune['nom'], updated_commune['cdp'])
        return redirect(url_for('commune.index'))