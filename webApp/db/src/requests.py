from db.src.dataBase import *
import shortuuid

#------------------------------------------------------------------------------------------------------#
#                                           Reqêtes générales                                          #
#------------------------------------------------------------------------------------------------------#

def lire_all(table:str):
    return r_requete(f"SELECT * FROM {table}")

def lire_by_id(table:str, tag:str, id:int):
    return r_requete(f"SELECT * FROM {table} WHERE {tag}=?", (id,))[0]

def lire_list_by_id(table:str, tag:str, id:int):
    return r_requete(f"SELECT * FROM {table} WHERE {tag}=?", (id,))

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

def insert_employe(new_employeId, new_employe):
    w_requete("INSERT INTO Employe (employeId, communeId, nom, prenom, ddn, adresse) VALUES (?, ?, ?, ?, ?, ?)", 
        (new_employeId, new_employe['communeId'], new_employe['nom'], new_employe['prenom'], new_employe['ddn'], new_employe['adresse']))

def update_employe(updated_employeId, updated_employe):
    w_requete("UPDATE Employe SET communeId=?, nom=?, prenom=?, ddn=?, adresse=? WHERE employeId=?;",
        (updated_employe['communeId'], updated_employe['nom'], updated_employe['prenom']
            , updated_employe['ddn'], updated_employe['adresse'], updated_employeId))

def delete_employe(id): 
    delete_by_id("Employe", "employeId", id)
    delete_by_id("Travailler", "employeId", id)

def lire_employe_full(id): return lire_list_by_id("Employe_full", "employeId", id)

def lire_employe_services(id): return lire_travailler_by_employeId(id)

def lire_employe(id): return lire_by_id("Employe", "employeId", id)

def lire_employes(): return lire_all("Employe_full")

#------------------------------------------------------------------------------------------------------#
#                                    Actions sur la table travailler                                   #
#------------------------------------------------------------------------------------------------------#

def insert_travailler(employeId, serviceId):
    try:
        w_requete("INSERT INTO Travailler (employeId, serviceId) VALUES (?, ?)", (employeId, serviceId))
    except sql.IntegrityError as err:
        print(err)
        return err

def delete_travailler(employeId, serviceId):
    w_requete(f"DELETE FROM Travailler WHERE employeId=? AND serviceId=?",(employeId, serviceId))

def update_travailler(id, travailler_to_add, travailler_to_del):
    for t_del in travailler_to_del:
        delete_travailler(id, t_del)
    for t_add in travailler_to_add:
        insert_travailler(id, t_add)
        
def lire_travailler_by_employeId(id): return lire_list_by_id("Travailler", "employeId", id)


#------------------------------------------------------------------------------------------------------#
#                                    Actions sur la table service                                      #
#------------------------------------------------------------------------------------------------------#

def insert_service(nom:str):
    w_requete("INSERT INTO Service (nom) VALUES (?)", (nom,))

def update_service(id:int, nom:str):
    w_requete("UPDATE Service SET nom=? where serviceId=?;", (nom, id))

def delete_service(id): delete_by_id("Service", "serviceId", id)

def lire_service(id): return lire_by_id("Service", "serviceId", id)

def lire_services(): return lire_all("Service")