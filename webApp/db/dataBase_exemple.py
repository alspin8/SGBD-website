import sqlite3 as sql

liste={}
liste["article"]=[["nom","text"],["prix","number"]]
liste["commande"]=[["dateCommande","date"]]

def lireColonne(nomTable):   
    return liste[nomTable]

def initialiser():
    con = sql.connect('database.db')
    con.execute('PRAGMA foreign_keys="1"')
    con.execute('PRAGMA secure_delete="1"')

def executerRequete(requete,remplacement=()):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(requete,remplacement)
    con.commit()
    con.close()

def lireRequete(requete,remplacement=()):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(requete,remplacement)
    return cur.fetchall()

def detruireTables():
    executerRequete("drop table if exists contenir")
    executerRequete("drop table if exists commande")
    executerRequete("drop table if exists article")

def creerTables():
    executerRequete('''create table if not exists article (
        idArticle integer primary key,
        nom varchar not null,
        prix real default 3);''')
    executerRequete('''create table if not exists commande (
        idCommande integer primary key,
        dateCommande date not null
    );''')
    executerRequete('''create table if not exists contenir (
        idCommande integer,
        idArticle integer,
        quantite integer not null,
        foreign key(idCommande) references Commande ON DELETE RESTRICT,
        foreign key(idArticle) references Article ON DELETE RESTRICT,
        primary key(idCommande,idArticle)
    );''')

def creerVues():
    executerRequete('''create view if not exists idCommandePrix(idCommande,prix) AS
    select commande.idCommande,SUM(article.prix*contenir.quantite) from commande
    inner join Contenir on commande.idCommande=Contenir.idCommande
    inner join Article on Contenir.idArticle=Article.idArticle
    group by(commande.idCommande)
    ''')

def lireMaxId(table):
    return lireRequete("SELECT MAX(id"+table+") from "+table+';')[0][0]

def insertArticle(id,nom,prix):
    executerRequete("INSERT INTO Article (idArticle,nom,prix) VALUES (?,?,?)", 
                    (id,nom,prix))

def effacerArticle(id):
    executerRequete("DELETE FROM Article WHERE idArticle=?",(id,))
    
def updateArticle(id,nom,prix):
    executerRequete("UPDATE Article SET nom=?,prix=? where idArticle=?;",
                    (nom,prix,id))

def insertCommande(id,date):
    executerRequete("INSERT INTO Commande (idCommande,dateCommande) VALUES (?,?)",
                    (id,date))

def insertArticleDansCommande(idCommande,idArticle,quantite):
    executerRequete("INSERT INTO Contenir (idCommande,idArticle,quantite) VALUES (?,?,?)",
                    (idCommande,idArticle,quantite))

def effacerArticleDansCommande(idCommande,idArticle):
    executerRequete('''DELETE FROM Conteninumberr WHERE idCommande=? AND idArticle=?;''',
                    (idCommande,idArticle))

def updateArticleDansCommande(idCommande,idArticle,quantite):
    executerRequete("UPDATE FROM Contenir SET quantite=? WHERE idCommande=? AND idArticle=?;",
                    (quantite,idCommande,idArticle))

def articleDansCommande(idCommande):
    liste=lireRequete('''SELECT nom from Article INNER JOIN Contenir ON Article.idArticle=Contenir.idArticle
                    INNER JOIN Commande ON Commande.idCommande=Contenir.idCommande
                    WHERE Commande.idCommande=? ASC Article.nom''',(str(idCommande)))
    tab=[]
    for i in liste:
        tab.append(i[0])
    return tab

def articlePasDansCommande(idCommande):
    liste=lireRequete('''SELECT nom FROM Article EXCEPT
                    SELECT nom from Article INNER JOIN Contenir ON Article.idArticle=Contenir.idArticle
                    INNER JOIN Commande ON Commande.idCommande=Contenir.idCommande
                    WHERE Commande.idCommande=?''',(str(idCommande)))
    tab=[]
    for i in liste:
        tab.append(i[0])
    return tab

#renvoie un tableau de tuple [('Chaussure,)] par exemple d'ou le [0][0]
def nomArticleParId(id):
    return lireRequete("SELECT nom FROM Article WHERE idArticle=?",(str(id)))[0][0]

def idArticleParNom(nom):
    return lireRequete("SELECT idArticle FROM Article WHERE nom='"+nom+"';")[0][0]

def prixCommande(id):
    prix=lireRequete("SELECT prix from idCommandePrix where idCommande="+str(id))
    if len(prix)==0:
        return 0
    else:
        return prix[0][0]

def dateCommande(id):
    return lireRequete("SELECT dateCommande from commande where idCommande="+str(id))[0][0]

def idNomPrixQuantiteArticleDansCommande(id):
    return lireRequete('''select article.idArticle,article.nom,article.prix,contenir.quantite from commande
                                inner join Contenir on commande.idCommande=Contenir.idCommande
                                inner join Article on Contenir.idArticle=Article.idArticle
                                where commande.idCommande='''+id)


def supprimerTableID(table, id):
    executerRequete("DELETE from "+str(table)+" WHERE id"+str(table)+"="+str(id))

def effacerCommande(idCommande):
    executerRequete("DELETE FROM Contenir WHERE idCommande=?",(idCommande,))
    executerRequete("DELETE FROM Commande WHERE idCommande=?",(idCommande,))

def effacerTables():
    executerRequete('''DELETE FROM Contenir;''')
    executerRequete('''DELETE FROM Article;''')
    executerRequete('''DELETE FROM Commande;''')

def remplirTables():
    effacerTables()
    insertArticle(1,'aze',45)
    insertArticle(2,'Veste',45)
    insertArticle(3,'Feutre',5)
    insertArticle(4,'Bottes',35)
    insertArticle(5,'test',78)

    effacerArticle(5)
    updateArticle(1,'Chaussure',25)

    insertCommande(1,'20/01/2018')
    insertCommande(2,'18/02/2017')
    insertCommande(3,'11/02/2017')
    insertArticleDansCommande(3,1,3)
    insertArticleDansCommande(3,2,2)
    
    effacerCommande(3)

    insertArticleDansCommande(1,1,3)
    insertArticleDansCommande(1,2,2)
    
    insertArticleDansCommande(2,1,5)
    insertArticleDansCommande(2,2,7)
    insertArticleDansCommande(2,3,3)
    insertArticleDansCommande(2,4,2)

