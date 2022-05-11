from utils import get_dict_from_jsonfile
import sqlite3 as sql

#------------------------------------------------------------------------------------------------------#
#                                         Lecture des modèles                                          #
#------------------------------------------------------------------------------------------------------#

tables = get_dict_from_jsonfile("db/model.json")["tables"]
views = get_dict_from_jsonfile("db/model.json")["views"]
db = 'db/database.db'

#------------------------------------------------------------------------------------------------------#
#                                      Initialisation de la base                                       #
#------------------------------------------------------------------------------------------------------#
def initialiser():
    con = sql.connect(db)
    con.execute('PRAGMA foreign_keys="1"')
    con.execute('PRAGMA secure_delete="1"')

#------------------------------------------------------------------------------------------------------#
#                                         Templates de requête                                         #
#------------------------------------------------------------------------------------------------------#

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