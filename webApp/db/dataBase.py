from utils import get_dict_from_jsonfile
import sqlite3 as sql

tables = get_dict_from_jsonfile("db/model.json")
db = 'db/database.db'

#  Template de requêtes
def initialiser():
    con = sql.connect(db)
    con.execute('PRAGMA foreign_keys="1"')
    con.execute('PRAGMA secure_delete="1"')

def w_requete(requete,remplacement=()):
    con = sql.connect(db)
    cur = con.cursor()
    cur.execute(requete,remplacement)
    con.commit()
    con.close()

def r_requete(requete,remplacement=()):
    con = sql.connect(db)
    cur = con.cursor()
    cur.execute(requete,remplacement)
    return cur.fetchall()

def lire_all(table:str):
    return r_requete(f"SELECT * FROM {table}")

def lire_by_id(table:str, tag:str, id:int):
    return r_requete(f"SELECT * FROM {table} WHERE {tag}=?", (id,))[0]

def delete_by_id(table:str, tag:str, id:int):
    w_requete(f"DELETE FROM {table} WHERE {tag}=?",(id,))

# Actions sur la table commune
def insert_commune(nom:str, cdp:str):
    w_requete("INSERT INTO Commune (nom, cdp) VALUES (?, ?)", (nom, cdp))

def update_commune(id:int, nom:str, cdp:str):
    w_requete("UPDATE Commune SET nom=?,cdp=? WHERE communeId=?;", (nom, cdp, id))

# Actions sur la table employe
def insert_employe(communeId:int, serviceId:str, nom:str, prenom:str, ddn, adresse:str):
    insert_travailler(employe_next_id(), serviceId)
    w_requete("INSERT INTO Employe (communeId, nom, prenom, ddn, adresse) VALUES (?, ?, ?, ?, ?)", 
        (communeId, nom, prenom, ddn, adresse))

def update_employe(id, communeId:int, serviceId:str, nom:str, prenom:str, ddn, adresse:str):
    # update_travailler(id, serviceId)
    w_requete("INSERT INTO Employe (communeId, nom, prenom, ddn, adresse) VALUES (?, ?, ?, ?, ?)", 
        (communeId, nom, prenom, ddn, adresse))

def employe_next_id():
    next_id = r_requete("SELECT MAX(employeId) AS max_id FROM Employe")[0][0]
    if next_id == None: return 1
    return next_id + 1

def lire_employe():
    return r_requete(
        """
        SELECT Employe.employeId, Employe.nom, Employe.prenom, Employe.ddn, Employe.adresse, Commune.nom, Service.nom FROM Employe
        INNER JOIN Commune ON Employe.communeId=Commune.communeId
        INNER JOIN Travailler ON Employe.employeId=Travailler.employeId
        INNER JOIN Service ON Travailler.serviceId=Service.serviceId
        """
    )

# Actions sur la table travailler
def insert_travailler(employeId:int, serviceId:int):
    w_requete("INSERT INTO Travailler (employeId, serviceId) VALUES (?, ?)", (employeId, serviceId))

# def update_travailler(employeId, serviceId, new_serviceId):
#     w_requete("UPDATE Travailler SET serviceId=? WHERE employeId=? AND serviceId=?", (new_serviceId, employeId, serviceId))

# Actions sur la table service
def insert_service(nom:str):
    w_requete("INSERT INTO Service (nom) VALUES (?)", (nom,))

def update_service(id:int, nom:str):
    w_requete("UPDATE Service SET nom=? where serviceId=?;", (nom, id))

# Management des tables
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

    insert_employe(1, 1, "Alex", "Clorennec", "08/08/2000", "Plozevet")
    insert_employe(7, 3, "Jean", "Massiet", "01/11/1987", "Douarnenez")