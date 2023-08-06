# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 12:03:13 2021

@author: Michael Nauge (Université de Poitiers)
"""


import requests
import json

from NklResponse import NklResponse

def get_collections(nklTarget, identifier, metadataFormat="--"):
    """
    Récupération des informations sur une collection.
    Retourne l'ensemble des informations relatives à la collection
        
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un COLLECTION identifier nakala.
        
    metadataFormat : STR
        une valeur de la liste ("--","dc", "qdc")
        
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
        NklResponse.dictVals : un dictionnaire contenant les metacollections obtenus depuis la reponse json du server

        
    """
    
    url = nklTarget.API_URL+"/collections/"+identifier
    if (metadataFormat=="qdc") or (metadataFormat=="dc"):
        url+="?metadata-format="+metadataFormat
        
    APIheaders = {}
    
    # on gère le cas où la collection est public
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
            nklR.message="Informations sur la collection"
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


    
def put_collections(nklTarget, identifier, dictVals):
    """
    Modification des informations d'une collection.
    Les informations à modifier doivent être dans le dictionnaire dictVals
    qui sera converti en objet json
    
        
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala
        
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
        NklResponse.dictVals : un dictionnaire contenant les metacollections obtenus depuis la reponse json du server

        
    """
    
    url = nklTarget.API_URL+"/collections/"+identifier
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
        
        # 204 le serveur a bien appliqué la modification
        if response.status_code == 204:
            nklR.isSuccess = True
            nklR.message="La collection a été modifiée"
            # ne retourne pas d'objet json en cas de réussite
            
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



def delete_collections(nklTarget, identifier):
    """
    Suppression d'une collection
	Supprime définitivement la collection.
	Les données contenues dans la collection ne seront pas supprimées
	notes : il est possible aussi de faire simplement quelques modifications avec les fonctions put_collections
    
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un COLLECTION identifier nakala
    
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
    
    url = nklTarget.API_URL+"/collections/"+identifier
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
        
        # 204 le serveur a bien supprimé la data
        if response.status_code == 204:
            nklR.isSuccess = True
            nklR.message="La collection a été supprimée"
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
    

def post_collections(nklTarget, data):
    """
    Création d'une nouvelle collection
    
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    data : DICT
        une instance d'un dictionaire python (qui sera converti en json) contenant les 
        clé-valeurs compatibles avec nakala
        Pour plus d'informations sur les valeurs possibles à mettre 
        dans le dictionnaire :
            https://apitest.nakala.fr/doc#operations-collections-post_collections
        ex : {
			  "status": "public",
			  "metas": [
				{
				  "value": "string",
				  "lang": "string",
				  "typeUri": "string",
				  "propertyUri": "string"
				}
			  ],
			  "datas": [
				"string"
			  ],
			  "rights": [
				{
				  "id": "string",
				  "role": "string"
				}
			  ]
			}
    
    """
    
    url = nklTarget.API_URL+"/collections"
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
            nklR.message="La collection a été correctement créée"
            # on converti l'objet json retournée en dictionnaire python
            nklR.dictVals = json.loads(response.text)
            # tout c'est bien passé donc on a un 
            # data identifier(DOI) à récupérer dans le json retourné par le server
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
    

def get_collections_datas(nklTarget, identifier, page=1, limit=10):
    """
    Récupération de la liste paginée des données contenues dans la collection
        
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un COLLECTION identifier nakala.
        
    page : INT
        La page souhaitée
    
    limit : INT
        Le nombre de résultat par page
        
        
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
        NklResponse.dictVals : un dictionnaire contenant les metacollections obtenus depuis la reponse json du server

        
    """
    #​/collections​/{identifier}​/datas

    url = nklTarget.API_URL+"/collections/"+identifier+"/datas?page="+str(page)+"&limit="+str(limit)
    

    APIheaders = {}
    
    # on gère le cas où la collection est public
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
            nklR.message="Informations sur la collection"
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



def post_collections_datas(nklTarget, identifier, datas):
    """
    Ajout d'une liste de données dans une collection  
    
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un COLLECTION identifier nakala.
    
    datas : Liste des identifiants des données à ajouter à la collection
        ex : [
            "10.34847/nkl.12345678",
            "10.34847/nkl.fedcba98"
            ]
    """
    
    url = nklTarget.API_URL+"/collections/"+identifier+"/datas"
    APIheaders = {}
    
    # on gère le cas où il n'y a pas de API_KEY ce qui posera problème au server
    # mais il nous le fera savoir !
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL,"accept": "application/json", "Content-Type": "application/json"}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        response = requests.post(url, data =json.dumps(datas), headers=APIheaders)

        # on récupère le code
        nklR.code = response.status_code
        
        # 201 le serveur a bien répondu
        if response.status_code == 201:
            nklR.isSuccess = True
            nklR.message="Les données ont été ajoutées à la collection"
            # on converti l'objet json retournée en dictionnaire python
            nklR.dictVals = json.loads(response.text)
            
            return nklR
        
        else:
            
            dicError = json.loads(response.text)
            nklR.message=dicError['message']

        
    except requests.exceptions.RequestException as e:
        nklR.code=-1
        nklR.message=e
        
    #on retourne l'objet NklResponse avec erreur (de nakala ou de connexion reseau)
    return nklR