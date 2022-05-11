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
    w_requete('''DROP VIEW IF EXISTS Employe_full;''')

#------------------------------------------------------------------------------------------------------#
#                                        Remplissage des tables                                        #
#------------------------------------------------------------------------------------------------------#

def remplir_tables():
    insert_service("RESSOURCES HUMAINES")
    insert_service("FINANCES ET COMMANDE PUBLIQUE")
    insert_service("AMÉNAGEMENT ET ENVIRONNEMENT TERRITORIAL")
    insert_service("ACTION SOCIALE INTERCOMMUNALE")

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

    id = str(shortuuid.uuid()[:12])
    insert_employe(id, 1, "Alex", "Clorennec", "08/08/2000", "Plozevet")
    insert_travailler(id, 3)
    insert_travailler(id, 4)
    id = str(shortuuid.uuid()[:12])
    insert_employe(id, 3, "Jean", "Massiet", "01/11/1987", "Douarnenez")
    insert_travailler(id, 1)