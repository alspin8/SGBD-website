from multiprocessing import Value
from db.src.requests import *

#------------------------------------------------------------------------------------------------------#
#                                                Employés                                              #
#------------------------------------------------------------------------------------------------------#


def get_employe_count(): return r_requete("SELECT COUNT(*) FROM Employe")[0][0]

def employe_in_most_services():
    return r_requete(
        """
        SELECT Employe.nom, Employe.prenom FROM Employe
	        INNER JOIN EmployeIdNbService ON Employe.employeId=EmployeIdNbService.employeId
	        WHERE EmployeIdNbService.nbService=(SELECT MAX(EmployeIdNbService.nbService) FROM EmployeIdNbService)
        """
    )[0]

def oldest_employe():
    return r_requete(
        """
        SELECT AVG(EmployeIdAge.age) FROM EmployeIdAge
        """
    )[0][0]

def employes_living_working_in_same_town():
    return r_requete(
        """
        SELECT Employe.nom, Employe.prenom, Employe.adresse FROM Employe
	        INNER JOIN Commune ON Employe.communeId=Commune.communeId
	        WHERE UPPER(Commune.nom)=UPPER(Employe.adresse)
        """
    )

#------------------------------------------------------------------------------------------------------#
#                                                Communes                                              #
#------------------------------------------------------------------------------------------------------#


def get_commune_count(): return r_requete("SELECT COUNT(*) FROM Commune")[0][0]

def get_most_populated_commune():
    return r_requete(
        """
        SELECT NomCommuneNbEmploye.nom FROM NomCommuneNbEmploye
	        WHERE NomCommuneNbEmploye.nbEmploye=(SELECT MAX(NomCommuneNbEmploye.nbEmploye) FROM NomCommuneNbEmploye)
        """
    )[0][0]

def get_less_populated_commune():
    return r_requete(
        """
        SELECT NomCommuneNbEmploye.nom FROM NomCommuneNbEmploye
	        WHERE NomCommuneNbEmploye.nbEmploye=(SELECT MIN(NomCommuneNbEmploye.nbEmploye) FROM NomCommuneNbEmploye)
        """
    )[0][0]

def get_percent_employe_per_commune():
    return r_requete(
        """
        SELECT NomCommuneNbEmploye.nom, 
        (NomCommuneNbEmploye.nbEmploye*100/(SELECT SUM(NomCommuneNbEmploye.nbEmploye) FROM NomCommuneNbEmploye)) AS Percent
        FROM NomCommuneNbEmploye
        """
    )

#------------------------------------------------------------------------------------------------------#
#                                                Services                                              #
#------------------------------------------------------------------------------------------------------#


def get_service_count(): return r_requete("SELECT COUNT(*) FROM Service")[0][0]


def get_most_populated_service():
    return r_requete(
    """
    SELECT NomServiceNbEmploye.nom FROM NomServiceNbEmploye
	    WHERE NomServiceNbEmploye.nbEmploye=(SELECT MAX(NomServiceNbEmploye.nbEmploye) FROM NomServiceNbEmploye)
    """
    )[0][0]

def get_less_populated_service():
    return r_requete(
        """
        SELECT NomServiceNbEmploye.nom FROM NomServiceNbEmploye
	        WHERE NomServiceNbEmploye.nbEmploye=(SELECT MIN(NomServiceNbEmploye.nbEmploye) FROM NomServiceNbEmploye)
        """
    )[0][0]


def get_percent_employe_per_service(): 
    return r_requete(
        """
        SELECT NomServiceNbEmploye.nom, 
	    (NomServiceNbEmploye.nbEmploye*100/(SELECT SUM(NomServiceNbEmploye.nbEmploye) FROM NomServiceNbEmploye)) AS Percent
        FROM NomServiceNbEmploye

        """
    )

#------------------------------------------------------------------------------------------------------#
#                                  Mise en forme sous forme de dictionnaire                            #
#------------------------------------------------------------------------------------------------------#


def get_stats():
    stats = (
        {
            'employe':
            [
                {
                    'title': 'Statistiques générales',
                    'cards':
                    [
                        {
                        'value': get_employe_count(),
                        'description': "Employés"
                        },
                        {
                            'value': f"{employe_in_most_services()[1]} {employe_in_most_services()[0]}",
                            'description': "Employé dans le plus de services"
                        },
                        {
                            'value': f"{round(oldest_employe(), 2)} ans",
                            'description': "Moyenne d'age des employés"
                        }
                    ]
                },
                {
                    'title': "Employés habitant et travaillant dans la même ville",
                    'cards':
                    [

                    ]

                }
            ],
            'commune':
            [
                {
                    'title': 'Statistiques générales',
                    'cards':
                    [
                        {
                        'value': get_commune_count(),
                        'description': "Communes"
                        },
                        {
                        'value': get_most_populated_commune(),
                        'description': "Le plus d'employés"
                        },
                        {
                        'value': get_less_populated_commune(),
                        'description': "Le moins d'employés"
                        }
                    ]
                },
                {
                    'title': "Répartition des employés par commune",
                    'cards':
                    [

                    ]

                }
            ],
            'service':
            [
                {
                    'title': 'Statistiques générales',
                    'cards':
                    [
                        {
                        'value': get_service_count(),
                        'description': "Services"
                        },
                        {
                        'value': get_most_populated_service(),
                        'description': "Le plus d'employés"
                        },
                        {
                        'value': get_less_populated_service(),
                        'description': "Le moins d'employés"
                        }
                    ]
                },
                {
                    'title': "Répartition des employés par service",
                    'cards':
                    [

                    ]

                }
            ]
        }
    )
    percent_employe_per_service = get_percent_employe_per_service()
    for item in percent_employe_per_service:
        stats['service'][1]['cards'].append(
            {
                'value': f"{item[1]} %",
                'description': item[0]
            }
        )

    percent_employe_per_commune = get_percent_employe_per_commune()
    for item in percent_employe_per_commune:
        stats['commune'][1]['cards'].append(
            {
                'value': f"{item[1]} %",
                'description': item[0]
            }
        )

    employe_living_working = employes_living_working_in_same_town()
    for item in employe_living_working:
        stats['employe'][1]['cards'].append(
            {
                'value': f"{item[1]} {item[0]}",
                'description': item[2]
            }
        )
    
    return stats

