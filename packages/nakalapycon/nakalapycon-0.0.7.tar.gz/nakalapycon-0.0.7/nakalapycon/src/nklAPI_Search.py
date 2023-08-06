# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:16:50 2022

@author: Michael Nauge (Université de Poitiers)

"""


import requests
import json

from NklResponse import NklResponse


def get_search_datas(nklTarget, q="", fq="", facet="", order="relevance"):
    """
    Recherche des données Nakala.
    Retourne des données Nakala en fonction de critères de recherche
    
    Attention, cette fonction retourne également des collections. 
    Mais les colletions trouvées n'ont pas de key files mais une key dataids
    Pour préciser et contraindre à n'obtenir que 
        des datas il faut préciser en paramètre fq = scope=data
        des collections il faut préciser en paramètre fq = scope=collection
    
        
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    q : STR
    	requête à effectuer
        
    fq : STR
        filtres pour la requête
        Filtres disponibles : scope, status, type, year, created, language, collection, license, fileExt, depositor, owner et share
        Il est possible de rechercher sur plusieurs filtres ; le caractère de séparation est le point-virgule. La recherche est traduite par un ET entre les filtres.
        Il est possible d'ajouter plusieurs valeurs pour un même filtre ; le caratère de séparation est la virgule. La recherche se fera alors par un OU entre les valeurs.
        Exemple : scope=collection;status=public;year=2009,1889
        
        
        
    facet : STR
        facette(s) à retourner
        Facettes disponibles : scope, status, type, year, created, license, language, fileExt, fileSize, fileType et collection
        Il est possible de retrouner plusieurs facettes ; le caractère de séparation est le point-virgule.
        Il est possible de configurer la taille et l'ordre d'une facette avec les paramètres size, sort et order
        Pour la facette created, size correspond au format date souhaité : yyyy, yyyy-MM ou yyyy-MM-dd
        Exemple : type,size=17,sort=item,order=asc;fileExt,size=7,sort=count,order=desc
        
        
    order : STR
         tri des résultats
         Valeurs possibles : relevance ou date,desc ou date,asc ou title,desc ou title,asc
         
        
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
    
    url = nklTarget.API_URL+"/search?"
    
    #ajout des paremtres de filtre
    url += "q="+q
    url += "&fq="+fq
    url += "&facet="+facet
    url + "&order="+order
    
    
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
            nklR.message="Retourne une liste de données"
            # on converti l'objet json retournée en dictionnaire python
            nklR.dictVals = json.loads(response.text)
            
            # on retourne l'objet NklResponse maintenant entièrement rempli
            return nklR
        
        else:
            
            if 'text' in response:
                dicError = json.loads(response.text)
                nklR.message=dicError['message']
            

        
    except requests.exceptions.RequestException as e:
        nklR.code=-1
        nklR.message=e
        
    #on retourne l'objet NklResponse avec erreur (de nakala ou de connexion reseau)
    return nklR


def get_search_authors(nklTarget, q="", order="asc", page="1", limit="10"):
    """
    Récupération des auteurs associés aux données de Nakala.
    Retourne des auteurs associés aux données de Nakala en fonction de critères de recherche
        
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    q : STR
    	Mot clé pour la recherche
                
        
    order : STR
        Sens du tri (basé le prénom puis le nom de famille)
        Valeurs possibles : desc ou asc
         
    page : STR
        Page courante
         
    limit : STR
    
        
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
    
    url = nklTarget.API_URL+"/authors/search?"
    
    #ajout des paremtres de filtre
    url += "q="+q
    url + "&order="+order
    url + "&page="+page
    url + "&limit="+limit
    
    
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
            nklR.message="Retourne une liste d'auteurs"
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
