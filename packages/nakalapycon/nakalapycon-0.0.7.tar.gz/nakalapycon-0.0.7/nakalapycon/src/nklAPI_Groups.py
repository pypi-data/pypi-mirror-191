# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 15:50:10 2021

@author: Michael Nauge (Université de Poitiers)
"""

import requests
import json

from NklResponse import NklResponse


def search_groups(nklTarget, q, order="asc", page=1, limit=10):
    """
    Récupération des utilisateurs et groupes d'utilisateurs
    Retourne des utilisateurs et groupes d'utilisateurs en fonction de critères de recherche
    
    Parameters
    ----------
    nklTarget : TYPE
        une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    q : STR
        Mot clé pour la recherche
        
    order : STR
        Sens du tri (basé le prénom puis le nom de famille)
        
    page : STR
        Page courante
        
    limit : STR
        Nombre de résultats par page
    
    

    Returns
    -------
    NklResponse : OBJ
        une instance d'un objet NklResponse
        - en cas de problème reseau ou de message d'erreur du serveur nakala
        l'objet NklResponse.isSuccess=False et le détails de l'erreur en version textuel
        sera dans NklResponse.message
        
        - en cas de réussite de la requete
        l'objet NklResponse.isSuccess=True et 
        les métadonnées reçu seront dans
        NklResponse.dictVals : un dictionnaire contenant les metadatas obtenus depuis la reponse json du server

    """
    
    url = nklTarget.API_URL+"/groups/search"
   
    #https://apitest.nakala.fr/groups/search?q=Huma-Num-test-Admin&order=asc&page=1&limit=10"
    url += "?q=" + q
    url += "&order=" + order
    url += "&page="+str(page)
    url += "&limit="+str(limit)
    
        
    APIheaders = {}
    
    # on gère le cas où la data est public
    # et qu'il n'y a donc pas besoin de API_KEY
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        response = requests.get(url, headers=APIheaders)
        # on récupère le code
        nklR.code = response.status_code
        
        # 200 le serveur a bien répondu
        if response.status_code == 200:
            nklR.isSuccess = True
            nklR.message="Retourne l'objet de la recherche"
            # on converti l'objet json retournée en dictionnaire python
            nklR.dictVals = json.loads(response.text)
            
            # on retourne l'objet NklResponse maintenant entièrement rempli
            return nklR
        
        else:
            
            dicError = json.loads(response.text)
            nklR.message=dicError['message']

        
    except requests.exceptions.RequestException as e:
        nklR.code=-1
        nklR.message=e
        
    #on retourne l'objet NklResponse avec erreur (de nakala ou de connexion reseau)
    return nklR    
    
    
        

def get_groups(nklTarget, identifier):
    """
    Récupération des informations d'un groups/liste d'utilistateurs.
    Retourne l'ensemble des informations relatives à ce group
        
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un groups identifier nakala. 
        exempe : cb5f5980-056e-11ec-9b31-52540084ccd3
        
        
    Returns
    -------
    NklResponse : OBJ
        une instance d'un objet NklResponse
        - en cas de problème reseau ou de message d'erreur du serveur nakala
        l'objet NklResponse.isSuccess=False et le détails de l'erreur en version textuel
        sera dans NklResponse.message
        
        - en cas de réussite de la requete
        l'objet NklResponse.isSuccess=True et 
        les métadonnées reçu seront dans
        NklResponse.dictVals : un dictionnaire contenant les metadatas obtenus depuis la reponse json du server

        
    """
    
    url = nklTarget.API_URL+"/groups/"+identifier
   
    
    APIheaders = {}
    
    # on gère le cas où la data est public
    # et qu'il n'y a donc pas besoin de API_KEY
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        response = requests.get(url, headers=APIheaders)
        # on récupère le code
        nklR.code = response.status_code
        
        # 200 le serveur a bien répondu
        if response.status_code == 200:
            nklR.isSuccess = True
            nklR.message="Retourne l'objet donnée"
            # on converti l'objet json retournée en dictionnaire python
            nklR.dictVals = json.loads(response.text)
            
            # on retourne l'objet NklResponse maintenant entièrement rempli
            return nklR
        
        else:
            
            dicError = json.loads(response.text)
            nklR.message=dicError['message']

        
    except requests.exceptions.RequestException as e:
        nklR.code=-1
        nklR.message=e
        
    #on retourne l'objet NklResponse avec erreur (de nakala ou de connexion reseau)
    return nklR


    
def put_groups(nklTarget, identifier, dictVals):
    """
    Le groupe utilisateur transmis dans dictVals remplacera celui déjà existant.
    Note: Il n'est pas possible de modifier des groupes de type "user".
    
        
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un groups identifier nakala
        
    dictVals : dict
        un dictionnaire à convertir en json compatible avec les clés et valeurs attendues par nakala
        

    Returns
    -------
    NklResponse : OBJ
        une instance d'un objet NklResponse
        - en cas de problème reseau ou de message d'erreur du serveur nakala
        l'objet NklResponse.isSuccess=False et le détails de l'erreur en version textuel
        sera dans NklResponse.message
        
        - en cas de réussite de la requete
        l'objet NklResponse.isSuccess=True et 
        les métadonnées reçu seront dans
        NklResponse.dictVals : un dictionnaire contenant les metadatas obtenus depuis la reponse json du server

        
    """
    
    url = nklTarget.API_URL+"/groups/"+identifier
    APIheaders = {}

    # on gère le cas où la data est public
    # et qu'il n'y a donc pas besoin de API_KEY
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL, "Content-Type": "application/json"}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        response = requests.put(url, data =json.dumps(dictVals), headers=APIheaders)

        # on récupère le code
        nklR.code = response.status_code
        
        # 200 le serveur a bien appliqué la modification
        # surprenant, habituellement ça retour un 204... (mail à huma-num)
        
        #if response.status_code == 204:
        if response.status_code == 200:
            nklR.isSuccess = True
            nklR.message="Le group a été modifiée"
            # ça ne retourne pas d'objet json en cas de réussite

            #print("response : ", response)

            # on retourne l'objet NklResponse maintenant entièrement rempli
            return nklR
        
        else:
            
            dicError = json.loads(response.text)
            nklR.message=dicError['message']

        
    except requests.exceptions.RequestException as e:
        nklR.code=-1
        nklR.message=e
        
    #on retourne l'objet NklResponse avec erreur (de nakala ou de connexion reseau)
    return nklR



def delete_groups(nklTarget, identifier):
    """
    Suppression d'un groupe d'utilisateurs
    La suppression d'un groupe entraine la suppression de tous les droits liés à ce groupe.
    Note: Il n'est pas possible de supprimer un groupe de type "user" ou un groupe propriétaire d'une donnée ou d'une collection
    
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala
    
    Returns
    -------
    NklResponse : OBJ
        une instance d'un objet NklResponse
        - en cas de problème reseau ou de message d'erreur du serveur nakala
        l'objet NklResponse.isSuccess=False et le détails de l'erreur en version textuel
        sera dans NklResponse.message
        
        - en cas de réussite de la requete
        l'objet NklResponse.isSuccess=True et 
        puisqu'il n'y a pas de retour json en cas de réussite 
        NklResponse.dictVals = {}
        
    """
    
    url = nklTarget.API_URL+"/groups/"+identifier
    APIheaders = {}
    
    # on gère le cas où il n'y a pas  de API_KEY
    # ce qui va poser problème pour le serveur nakala
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        response = requests.delete(url, headers=APIheaders)
        # on récupère le code
        nklR.code = response.status_code
        
        # 200 le serveur a bien supprimé la data
        # habituellement c'est 204 quand le serveur a bien supprimé 
        #if response.status_code == 204:
        if response.status_code == 200:
            nklR.isSuccess = True
            nklR.message="Le group a été supprimé"
            # Il n'y a pas d'objet json retournée à convertir en dictionnaire python
            
            # on retourne l'objet NklResponse maintenant rempli
            return nklR

        else:
            dicError = json.loads(response.text)
            nklR.message=dicError['message']

        
    except requests.exceptions.RequestException as e:
        nklR.code=-1
        nklR.message=e
        
    #on retourne l'objet NklResponse avec erreur (de nakala ou de connexion reseau)
    return nklR
    

def post_groups(nklTarget, data):
    """
    Permet de la création d'un nouveau groupe d'utilisateurs
    
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    data : DICT
        une instance d'un dictionaire python (qui sera converti en json) contenant les 
        clé-valeurs compatibles avec nakala
        Pour plus d'informations sur les valeurs possibles à mettre 
        dans le dictionnaire :
            https://apitest.nakala.fr/doc#operations-datas-post_groups
            
        ex :{
              "name": "HUMA-NUM",
              "users": [
                "pdupont",
                "jdubois",
                "lmartin"
              ]
            }
    
    """
    
    url = nklTarget.API_URL+"/groups"
    APIheaders = {}
    
    # on gère le cas où il n'y a pas de API_KEY ce qui posera problème au server
    # mais il nous le fera savoir !
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL,"accept": "application/json", "Content-Type": "application/json"}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        response = requests.post(url, data =json.dumps(data), headers=APIheaders)

        # on récupère le code
        nklR.code = response.status_code
        
        # 201 le serveur a bien répondu
        if response.status_code == 201:
            nklR.isSuccess = True
            nklR.message="Enregistrement du groupe"
            # on converti l'objet json retournée en dictionnaire python
            nklR.dictVals = json.loads(response.text)
            # tout c'est bien passé donc on a un 
            # le group identifier à récupérer dans le json retourné par le server
            # dans nklR.dictVals['payload']['id']
            # on retourne l'objet NklResponse maintenant entièrement rempli
            return nklR
        
        else:
            
            dicError = json.loads(response.text)
            nklR.message=dicError['message']

        
    except requests.exceptions.RequestException as e:
        nklR.code=-1
        nklR.message=e
        
    #on retourne l'objet NklResponse avec erreur (de nakala ou de connexion reseau)
    return nklR
    

 
 