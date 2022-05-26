#!/usr/bin/env python3
from flask import Flask
from db.src.tablesAndViews import *

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config/config.py")

    from routes.main import main
    app.register_blueprint(main)
    from routes.service import service
    app.register_blueprint(service, url_prefix='/service')
    from routes.commune import commune
    app.register_blueprint(commune, url_prefix='/commune')
    from routes.employe import employe
    app.register_blueprint(employe, url_prefix='/employe')
    from routes.stats import stats
    app.register_blueprint(stats, url_prefix='/stats')

    return app

def init_tables():
    initialiser()
    creer_tables()
    effacer_tables()
    supprimer_vues()
    creer_vues()
    remplir_tables()

if __name__ == "__main__":
    init_tables()

    app = create_app()   
    app.run(debug=True)