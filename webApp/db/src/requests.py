from db.src.dataBase import *
import shortuuid

#------------------------------------------------------------------------------------------------------#
#                                           Reqêtes générales                                          #
#------------------------------------------------------------------------------------------------------#

def lire_all(table:str):
    return r_requete(f"SELECT * FROM {table}")

def lire_by_id(table:str, tag:str, id:int):
    return r_requete(f"SELECT * FROM {table} WHERE {tag}=?", (id,))[0]

def delete_by_id(table:str, tag:str, id:int):
    w_requete(f"DELETE FROM {table} WHERE {tag}=?",(id,))

#------------------------------------------------------------------------------------------------------#
#                                     Actions sur la table commune                                     #
#------------------------------------------------------------------------------------------------------#

def insert_commune(nom:str, cdp:str):
    w_requete("INSERT INTO Commune (nom, cdp) VALUES (?, ?)", (nom, cdp))

def update_commune(communeId:int, nom:str, cdp:str):
    w_requete("UPDATE Commune SET nom=?,cdp=? WHERE communeId=?;", (nom, cdp, communeId))

def delete_commune(id): delete_by_id("Commune", "communeId", id)

def lire_commune(id): return lire_by_id("Commune", "communeId", id)

def lire_communes(): return lire_all("Commune")

#------------------------------------------------------------------------------------------------------#
#                                     Actions sur la table employe                                     #
#------------------------------------------------------------------------------------------------------#

def insert_employe(employeId:int, communeId:int, nom:str, prenom:str, ddn, adresse:str):
    w_requete("INSERT INTO Employe (employeId, communeId, nom, prenom, ddn, adresse) VALUES (?, ?, ?, ?, ?, ?)", 
        (employeId, communeId, nom, prenom, ddn, adresse))

def update_employe(employeId, communeId:int, nom:str, prenom:str, ddn, adresse:str):
    w_requete("UPDATE Employe SET communeId=?, nom=?, prenom=?, ddn=?, adresse=? WHERE employeId=?;"
        (communeId, nom, prenom, ddn, adresse, employeId))

def delete_employe(id): delete_by_id("Employe", "employeId", id)

def lire_employe(id): return lire_by_id("Employe_full", "employeId", id)

def lire_employes(): return lire_all("Employe_full")

#------------------------------------------------------------------------------------------------------#
#                                    Actions sur la table travailler                                   #
#------------------------------------------------------------------------------------------------------#

def insert_travailler(employeId:int, serviceId:int):
    w_requete("INSERT INTO Travailler (employeId, serviceId) VALUES (?, ?)", (employeId, serviceId))

def update_travailler(employeId, serviceId, new_serviceId):
    w_requete("UPDATE Travailler SET serviceId=? WHERE employeId=? AND serviceId=?", (new_serviceId, employeId, serviceId))


#------------------------------------------------------------------------------------------------------#
#                                    Actions sur la table service                                   #
#------------------------------------------------------------------------------------------------------#

def insert_service(nom:str):
    w_requete("INSERT INTO Service (nom) VALUES (?)", (nom,))

def update_service(id:int, nom:str):
    w_requete("UPDATE Service SET nom=? where serviceId=?;", (nom, id))

def delete_service(id): delete_by_id("Service", "serviceId", id)

def lire_service(id): return lire_by_id("Service", "serviceId", id)

def lire_services(): return lire_all("Service")