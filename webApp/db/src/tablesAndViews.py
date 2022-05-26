from db.src.dataBase import *
from db.src.requests import *

#------------------------------------------------------------------------------------------------------#
#                                       Initialisation des tables                                      #
#------------------------------------------------------------------------------------------------------#

def table_description(table):
    desc = f"CREATE TABLE IF NOT EXISTS {table['name']} ("
    for cols in table['cols']:
        desc += f"{cols['name']} {cols['param']}"
    for constraint in table['constraints']:
        desc += f"{constraint}"
    desc += ');'
    return desc

def creer_tables():
    for table in tables:
        w_requete(table_description(table))

def effacer_tables():
    w_requete('''DELETE FROM Commune;''')
    w_requete('''DELETE FROM Employe;''')
    w_requete('''DELETE FROM Travailler;''')
    w_requete('''DELETE FROM Service;''')

#------------------------------------------------------------------------------------------------------#
#                                       Initialisation des vues                                      #
#------------------------------------------------------------------------------------------------------#

def view_description(view):
    desc = f"CREATE VIEW IF NOT EXISTS {view['name']} AS "
    for line in view['request_line']:
        desc += line + " "
    return desc

def creer_vues():
    for view in views:
        w_requete(view_description(view))

def supprimer_vues():
    for view in views:
        w_requete(f"DROP VIEW IF EXISTS {view['name']};")

#------------------------------------------------------------------------------------------------------#
#                                        Remplissage des tables                                        #
#------------------------------------------------------------------------------------------------------#

def remplir_tables():
    # Ajout des services :
    insert_service("Ressources Humaines")
    insert_service("Finance et Commande Publique")
    insert_service("Aménagement et Environnement")
    insert_service("Action Sociale et Intercommunale")
    insert_service("Informatique")

    # Ajout des communes
    insert_commune("Plozevet", "29710")
    insert_commune("Gourlizon", "29710")
    insert_commune("Guiler-sur-Goyen", "29710")
    insert_commune("Landudec", "29710")
    insert_commune("Peumerit", "29710")
    insert_commune("Plogastel-Saint-Germain", "29710")
    insert_commune("Pouldrezic", "29710")
    insert_commune("Plonéour-Lanvern", "29720")
    insert_commune("Plovan", "29720")
    insert_commune("Tréogat", "29720")

    # Ajout des employés
    id = str(shortuuid.uuid()[:12])
    insert_employe(
        id, 
        {
            "communeId": 1,
            "prenom": "Alex",
            "nom": "Clorennec",
            "ddn": "08/08/2000",
            "adresse": "Plozevet"
        }
    )
    insert_travailler(id, 3)
    insert_travailler(id, 4)
    insert_travailler(id, 1)

    id = str(shortuuid.uuid()[:12])
    insert_employe(
        id, 
        {
            "communeId": 3,
            "prenom": "Jean",
            "nom": "Massiet",
            "ddn": "01/11/1987",
            "adresse": "Douarnenez"
        }
    )
    insert_travailler(id, 1)

    id = str(shortuuid.uuid()[:12])
    insert_employe(
        id, 
        {
            "communeId": 7,
            "prenom": "Jean",
            "nom": "Todt",
            "ddn": "26/06/1962",
            "adresse": "Pouldrezic"
        }
    )
    insert_travailler(id, 4)
    insert_travailler(id, 5)

    id = str(shortuuid.uuid()[:12])
    insert_employe(
        id, 
        {
            "communeId": 3,
            "prenom": "ObiWan",
            "nom": "Kenobi",
            "ddn": "18/02/1969",
            "adresse": "Plozevet"
        }
    )
    insert_travailler(id, 4)

    id = str(shortuuid.uuid()[:12])
    insert_employe(
        id, 
        {
            "communeId": 10,
            "prenom": "Jammi",
            "nom": "Lanister",
            "ddn": "02/04/1985",
            "adresse": "Quimper"
        }
    )
    insert_travailler(id, 2)

    id = str(shortuuid.uuid()[:12])
    insert_employe(
        id, 
        {
            "communeId": 5,
            "prenom": "John",
            "nom": "Snow",
            "ddn": "29/05/1990",
            "adresse": "Peumerit"
        }
    )
    insert_travailler(id, 5)

    id = str(shortuuid.uuid()[:12])
    insert_employe(
        id, 
        {
            "communeId": 3,
            "prenom": "Compte",
            "nom": "Doku",
            "ddn": "02/11/1966",
            "adresse": "Plonéour-Lanvern"
        }
    )
    insert_travailler(id, 5)
    insert_travailler(id, 3)

    id = str(shortuuid.uuid()[:12])
    insert_employe(
        id, 
        {
            "communeId": 8,
            "prenom": "Mace",
            "nom": "Winduw",
            "ddn": "16/09/1979",
            "adresse": "Plonéour-Lanvern"
        }
    )
    insert_travailler(id, 1)
    insert_travailler(id, 2)
    insert_travailler(id, 3)
    insert_travailler(id, 4)
    insert_travailler(id, 5)
