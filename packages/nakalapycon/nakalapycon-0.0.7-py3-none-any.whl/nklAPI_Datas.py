# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 15:50:10 2021

@author: Michael Nauge (Université de Poitiers)
"""

import requests
import json

from NklResponse import NklResponse


def get_datas(nklTarget, identifier, metadataFormat="--"):
    """
    Récupération des informations sur une donnée.
    Retourne l'ensemble des informations relatives à la donnée
        
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        
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
        NklResponse.dictVals : un dictionnaire contenant les metadatas obtenus depuis la reponse json du server

        
    """
    
    url = nklTarget.API_URL+"/datas/"+identifier
    if (metadataFormat=="qdc") or (metadataFormat=="dc"):
        url+="?metadata-format="+metadataFormat
    
    
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


    
def put_datas(nklTarget, identifier, dictVals):
    """
    Modification des informations d'une donnée.
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
        NklResponse.dictVals : un dictionnaire contenant les metadatas obtenus depuis la reponse json du server

        
    """
    
    url = nklTarget.API_URL+"/datas/"+identifier
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
        
        # 204 le serveur a bien appliqué la modificatin
        if response.status_code == 204:
            nklR.isSuccess = True
            nklR.message="La donnée a été modifiée"
            # ça ne retourne pas d'objet json en cas de réussite

            
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



def delete_datas(nklTarget, identifier):
    """
    La suppression d'une donnée est autorisée uniquement si la donnée n'est pas publiée
    
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
    
    url = nklTarget.API_URL+"/datas/"+identifier
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
            nklR.message="La data a été supprimé"
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
    

def post_datas(nklTarget, data):
    
    """
    Permet de déposer une donnée dans Nakala
    Les fichiers associés à la donnée sont à déposer avant via POST /uploads
    afin de connaitre leurs fileIdentifier SHA1
    
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    data : DICT
        une instance d'un dictionaire python (qui sera converti en json) contenant les 
        clé-valeurs compatibles avec nakala
        Pour plus d'informations sur les valeurs possibles à mettre 
        dans le dictionnaire :
            https://apitest.nakala.fr/doc#operations-datas-post_datas
        ex : {
              "status": "published",
              "metas": [
                {
                  "value": "string",
                  "lang": "string",
                  "typeUri": "string",
                  "propertyUri": "string"
                }
              ],
              "files": [
                {
                  "sha1": "string",
                  "description": "string",
                  "embargoed": "string"
                }
              ],
              "collectionsIds": [
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
    
    url = nklTarget.API_URL+"/datas"
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
            nklR.message="Enregistrement de la donnée"
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
    
    
def get_datas_files(nklTarget, identifier):
    """
    Permet d'obtenir l'ensemble des informations sur les fichiers associés à une donnée
    
    
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        

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

    url = nklTarget.API_URL+"/datas/"+identifier+"/files"
    APIheaders = {}
    
    # on gère le cas où il n'y a pas  de API_KEY
    # ce qui va poser problème pour le serveur nakala
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
            nklR.message="Liste des métadonnées des fichiers"
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
    

def post_datas_files(nklTarget, identifier, fileInfos):
    """
    Permet d'ajouter un fichier à une donnée.
    Attention, le fichier doit être déposé avant à l'aide de la requête POST /uploads

    
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        
    fileInfos : DICT
        une instance d'un dictionaire python (qui sera converti en json) contenant les 
        clé-valeurs compatibles avec nakala
        Pour plus d'informations sur les valeurs possibles à mettre 
        dans le dictionnaire :
            https://apitest.nakala.fr/doc#operations-datas-post_datas__identifier__files
        ex : {
              "sha1": "string",
              "description": "string",
              "embargoed": "string"
            }
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
    
    url = nklTarget.API_URL+"/datas/"+identifier+"/files"
    APIheaders = {}
    
    # on gère le cas où il n'y a pas de API_KEY ce qui posera problème au server
    # mais il nous le fera savoir !
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL,"accept": "application/json", "Content-Type": "application/json"}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        response = requests.post(url, data =json.dumps(fileInfos), headers=APIheaders)

        # on récupère le code
        nklR.code = response.status_code
        
        # 201 le serveur a bien répondu
        if response.status_code == 200:
            nklR.isSuccess = True
            nklR.message="Fichier ajouté"
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


def delete_datas_files(nklTarget, identifier, fileIdentifier):
    """
    La suppression d'un fichier ne peut se faire que sur une donnée non publiée
    
    TODO : à débugger car pour le moment la fonction ne semble pas fonctionner...
    

    Parameters
    ----------
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        
    fileIdentifier : STR
        un SHA1 file identifier de la data.


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


    url = nklTarget.API_URL+"/datas/"+identifier+"​/files​/"+fileIdentifier
    print(url)
    APIheaders = {}
    
    # on gère le cas où il n'y a pas  de API_KEY
    # ce qui va poser problème pour le serveur nakala
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL, "accept": "application/json", "Content-Type": "application/json"}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        response = requests.delete(url, headers=APIheaders)
        # on récupère le code
        nklR.code = response.status_code
        
        # 200 le serveur a bien répondu
        if response.status_code == 200:
            nklR.isSuccess = True
            nklR.message="Fichier supprimé de la donnée"
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
    

def get_datas_metadatas(nklTarget, identifier, metadataFormat="--"):

    """
    Récupération de la liste des métadonnées d'une donnée
    
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        
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
        NklResponse.dictVals : un dictionnaire contenant les metadatas obtenus depuis la reponse json du server

    """

    url = nklTarget.API_URL+"/datas/"+identifier+"/metadatas"
    
    if (metadataFormat=="qdc") or (metadataFormat=="dc"):
        url+="?metadata-format="+metadataFormat

    
    
    print(url)
    APIheaders = {}
    
    # on gère le cas où il n'y a pas  de API_KEY
    # ce qui va poser problème pour le serveur nakala
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
            nklR.message="Liste des métadonnées des fichiers"
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
    




def post_datas_metadatas(nklTarget, identifier, dictVals):
    """
    Ajout d'une nouvelle métadonnée à une donnée
    
    Parameters
    ----------
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        
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
        NklResponse.dictVals
    """

    url = nklTarget.API_URL+"/datas/"+identifier+"/metadatas"
    APIheaders = {}
    
    # on gère le cas où il n'y a pas de API_KEY ce qui posera problème au server
    # mais il nous le fera savoir !
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        response = requests.post(url, data =json.dumps(dictVals), headers=APIheaders)

        # on récupère le code
        nklR.code = response.status_code
        
        # 201 le serveur a bien répondu
        if response.status_code == 201:
            nklR.isSuccess = True
            nklR.message="La métadonnée a été ajoutée à la donnée"
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
    

def delete_datas_metadatas(nklTarget, identifier, dictVals):
    """
    Suppression de métadonnées pour une donnée
    Il est possible de passer un filtre dans le corps de la requête qui permettra de ne supprimer que certaines métadonnées
    Par exemple pour supprimer les dcterms:subject en anglais il faudra passer l'objet suivant:
    {"lang": "en", "propertyUri": "http://purl.org/dc/terms/subject"}
    
    Parameters
    ----------
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        
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

        ex: {
              "value": "string",
              "lang": "string",
              "typeUri": "string",
              "propertyUri": "string"
            }
    """
    
    url = nklTarget.API_URL+"/datas/"+identifier+"/metadatas"
    APIheaders = {}
    
    # on gère le cas où il n'y a pas de API_KEY ce qui posera problème au server
    # mais il nous le fera savoir !
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL, "accept": "application/json", "Content-Type": "application/json"}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        response = requests.delete(url, data =json.dumps(dictVals), headers=APIheaders)

        # on récupère le code
        nklR.code = response.status_code
        
        # 200 le serveur a bien répondu
        if response.status_code == 200:
            nklR.isSuccess = True
            nklR.message="Nombre de métadonnées supprimées"
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




def get_datas_rights(nklTarget, identifier):

    """
	Permet de retourner une liste contenant l'utilisateur ou le groupe d'utilisateurs et le droit sur la donnée 
	
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        
        

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

    url = nklTarget.API_URL+"/datas/"+identifier+"/rights"
    
    
    print(url)
    APIheaders = {}
    
    # on gère le cas où il n'y a pas  de API_KEY
    # ce qui va poser problème pour le serveur nakala
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
            nklR.message="Liste des utilisateurs et des groupes ayant des droits sur la donnée"
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
    




def post_datas_rights(nklTarget, identifier, dictVals):
    """
    Permet de rajouter des droits à un utilisateur ou un group d'utilisateurs sur une donnée.
	Les droits possibles sont :ROLE_OWNER, ROLE_ADMIN, ROLE_EDITOR, ROLE_READER, 
    
    Parameters
    ----------
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        
    dictVals : dict
        un dictionnaire à convertir en json compatible avec les clés et valeurs attendues par nakala
        ex: [
			  {
				"id": "b55e770c-849b-11ea-87ea-0242ac1b0003",
				"role": "ROLE_READER"
			  }
			]

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
        NklResponse.dictVals
    """

    url = nklTarget.API_URL+"/datas/"+identifier+"/rights"
    APIheaders = {}
    
    # on gère le cas où il n'y a pas de API_KEY ce qui posera problème au server
    # mais il nous le fera savoir !
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        response = requests.post(url, data =json.dumps(dictVals), headers=APIheaders)

        # on récupère le code
        nklR.code = response.status_code
        
        # 200 le serveur a bien répondu
        if response.status_code == 200:
            nklR.isSuccess = True
            nklR.message="Droits ajoutés sur la donnée"
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
    

def delete_datas_rights(nklTarget, identifier, dictVals):
    """
    Suppression des droits pour un utilisateur ou un groupe d'utilisateurs sur une donnée
    La suppression des droits d'une donnée est autorisée aux utilisateurs ayant les droits propriétaire ou administrateur.
	Il est possible de passer un filtre dans le corps de la requête qui permettra de ne supprimer que certains droits.
	Par exemple pour supprimer tous les éditeurs d'une donnée : {"role": "ROLE_EDITOR"}
	Note: le droit propriétaire (ROLE_OWNER) d'une donnée ne peut pas être supprimé.
    
    Parameters
    ----------
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        
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

        ex: {
				"id": "b55e770c-849b-11ea-87ea-0242ac1b0003",
				"role": "ROLE_READER"
			}
    """
    
    url = nklTarget.API_URL+"/datas/"+identifier+"/rights"
    APIheaders = {}
    
    # on gère le cas où il n'y a pas de API_KEY ce qui posera problème au server
    # mais il nous le fera savoir !
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL, "accept": "application/json", "Content-Type": "application/json"}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        response = requests.delete(url, data =json.dumps(dictVals), headers=APIheaders)

        # on récupère le code
        nklR.code = response.status_code
        
        # 200 le serveur a bien répondu
        if response.status_code == 200:
            nklR.isSuccess = True
            nklR.message="Droits supprimés"
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



def get_datas_collections(nklTarget, identifier):

    """
	Récupération de la liste des collections contenant la donnée
	
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        
        

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

    url = nklTarget.API_URL+"/datas/"+identifier+"/collections"
    
    
    print(url)
    APIheaders = {}
    
    # on gère le cas où il n'y a pas  de API_KEY
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
            nklR.message="La liste des collections"
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
    




def post_datas_collections(nklTarget, identifier, listVals):
    """
    Ajout d'une donnée dans un ensemble de collections
    
    Parameters
    ----------
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        
    listVals : list
		Liste des identifiants des collections à associer à la donnée
        
        ex: [
			"10.34847/nkl.12345678",
			"10.34847/nkl.fedcba98"
			]

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
        NklResponse.dictVals
    """

    url = nklTarget.API_URL+"/datas/"+identifier+"/collections"
    APIheaders = {}
    
    # on gère le cas où il n'y a pas de API_KEY ce qui posera problème au server
    # mais il nous le fera savoir !
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        response = requests.post(url, data =json.dumps(listVals), headers=APIheaders)

        # on récupère le code
        nklR.code = response.status_code
        
        # 201 le serveur a bien répondu
        if response.status_code == 201:
            nklR.isSuccess = True
            nklR.message="La donnée a été ajoutée dans les collections"
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
    

def delete_datas_collections(nklTarget, identifier, listVals):
    """
    Suppression d'une donnée d'un ensemble de collections
    
	L'utilisateur doit au minimum avoir les droits de lecture sur la donnée et être éditeur des différentes collections.
	Ni la donnée, ni les collections ne sont supprimées de NAKALA.

    Parameters
    ----------
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        
    listVals : LIST
        Liste des identifiants des collections d'où la donnée doit être supprimée
		ex: [
			"10.34847/nkl.12345678",
			"10.34847/nkl.fedcba98"
			]
        

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

        ex: {
				"id": "b55e770c-849b-11ea-87ea-0242ac1b0003",
				"role": "ROLE_READER"
			}
    """
    
    url = nklTarget.API_URL+"/datas/"+identifier+"/collections"
    APIheaders = {}
    
    # on gère le cas où il n'y a pas de API_KEY ce qui posera problème au server
    # mais il nous le fera savoir !
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL, "accept": "application/json", "Content-Type": "application/json"}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        response = requests.delete(url, data =json.dumps(listVals), headers=APIheaders)

        # on récupère le code
        nklR.code = response.status_code
        
        # 200 le serveur a bien répondu
        if response.status_code == 200:
            nklR.isSuccess = True
            nklR.message="La donnée a été supprimé des collections"
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




def get_datas_status(nklTarget, identifier):

    """
	Récupération du statut d'une donnée
	Retourne le statut de la donnée. Le statut peut être:
    pending : donnée déposée mais pas encore en ligne
    published : donnée publiée
    deleted : donnée supprimée
    old : ancienne version d'une donnée publiée
	
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala.
        
        

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
        Attention en cas de réussite dictVals n'est pas un dictionnaire mais simplement une string contrairement à beaucoup d'autres réponses

    """

    url = nklTarget.API_URL+"/datas/"+identifier+"/status"
    
    
    print(url)
    APIheaders = {}
    
    # on gère le cas où il n'y a pas  de API_KEY
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
            nklR.message="Statut de la donnée"
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



    
def put_datas_status(nklTarget, identifier):
    """
    Publication d'une donnée
    Permet de publier une donnée déposée (non encore publique)
    Attention cette opération n'est pas réversible
    
        
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
        les métadonnées reçu seront dans
        NklResponse.dictVals : un dictionnaire contenant les metadatas obtenus depuis la reponse json du server

        
    """
    
    url = nklTarget.API_URL+"/datas/"+identifier+"/status/published"
    APIheaders = {}

    # on gère le cas où la data est public
    # et qu'il n'y a donc pas besoin de API_KEY
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        response = requests.put(url, headers=APIheaders)

        # on récupère le code
        nklR.code = response.status_code
        
        # 204 le serveur a bien appliqué la modificatin
        if response.status_code == 204:
            nklR.isSuccess = True
            nklR.message="Status changé"
            # cas de réussite il n'y a rien dans response.txt
            #donc on laisse dictVals vide
            #nklR.dictVals = json.loads(response.text)
            
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



def get_datas_uploads(nklTarget):
    """
    Les fichiers déposés restent dans un espace temporaire le temps qu'ils soient associés à une donnée de Nakala ou soient automatiquement supprimés (toutes les 24 heures)
    Retourne Liste des objets fichiers déposés
        
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    

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
    
    url = nklTarget.API_URL+"/datas/uploads"
    APIheaders = {}
    
    # on gère le cas où il n'y a pas  de API_KEY
    # ce qui va poser problème pour le serveur nakala
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
            nklR.message="Liste des objets fichiers déposés"
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


def post_datas_uploads(nklTarget, pathFile):
    """
    Permet de déposer un fichier dans un espace temporaire de NAKALA pour 
    être ensuite associé à une donnée (requête POST /datas)
    
    Avant de pouvoir créer une data nakala contenant un fichier
    il faut avoir préalablement envoyé le fichier.
    
    Il faut donc utiliser cette fonction pour envoyer un fichier.
    Une fois le fichier reçu sur nakala, 
    le serveur nous retourne le SHA-1 du fichier.
    Ce fichier est stocké dans un espace temporaire de traitement.
    

    Parameters
    ----------
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    pathFile : STR
        le chemin local vers le fichier à envoyer.
    

    

    NklResponse : OBJ
        une instance d'un objet NklResponse
        - en cas de problème reseau ou de message d'erreur du serveur nakala
        l'objet NklResponse.isSuccess=False et le détails de l'erreur en version textuel
        sera dans NklResponse.message
        
        - en cas de réussite de la requete
        l'objet NklResponse.isSuccess=True et 
        les métadonnées reçu seront dans
        NklResponse.dictVals : un dictionnaire contenant les metadatas obtenus depuis la reponse json du server
        Le SHA1 est accessible dans NklResponse.dictVals['sha1']

    """
    
        
    url = nklTarget.API_URL+"/datas/uploads"
    APIheaders = {}
    
    # on gère le cas où la data est public
    # et qu'il n'y a donc pas besoin de API_KEY
    if nklTarget.apiKey_isEmpty()==False:
        APIheaders = {"X-API-KEY": nklTarget.API_KEY_NKL, "accept": "application/json"}      

    # création d'une instance d'un objet NklResponse à retourner
    nklR = NklResponse()

    try : 
        
        fileOpened = open(pathFile, "rb")    
        fileCur = {'file': fileOpened}
    
        response = requests.post(url, files=fileCur, headers=APIheaders)
        # on récupère le code
        nklR.code = response.status_code
        
        # 201 le serveur a bien répondu
        if response.status_code == 201:
            nklR.isSuccess = True
            nklR.message="Retourne l'empreinte SHA1 du fichier déposé sur le serveur"
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



    
    




def delete_datas_uploads(nklTarget, fileIdentifier):
    """
    Permet de supprimer un fichier présent dans l'espace temporaire
        
    Note : pour supprimer facilement tous les fichiers de l'espace temporaire
    nous recommendons l'utilisation de nklUtils.delete_datas_uploads_all(nklTarget)
    
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    
    Returns
    -------
    NklResponse : OBJ
        une instance d'un objet NklResponse
        - en cas de problème reseau ou de message d'erreur du serveur nakala
        l'objet NklResponse.isSuccess=False et le détails de l'erreur en version textuel
        sera dans NklResponse.message
        
        - en cas de réussite de la requete
        l'objet NklResponse.isSuccess=True et 
        pusiqu'il n'y a pas de retour json en cas de réussite 
        NklResponse.dictVals = {}
        
    """
    
    url = nklTarget.API_URL+"/datas/uploads/"+fileIdentifier
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
        
        # 200 le serveur a bien répondu
        if response.status_code == 200:
            nklR.isSuccess = True
            nklR.message="Le fichier a été supprimé"
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
    


def get_iiif_infoJson(nklTarget, identifier, fileIdentifier):
    """
    IIIF Image API - Information sur l'image "fileIdentifier" de la donnée "identifier"
        
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    identifier : STR
        un DATA identifier nakala
        
    fileIdentifier : STR
        un SHA1 file identifier de la data.

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
    
   
    
    url = nklTarget.API_URL+"/iiif/"+identifier+"/"+fileIdentifier+"/info.json"
    APIheaders = {}
    
    # on gère le cas où il n'y a pas  de API_KEY
    # ce qui va poser problème pour le serveur nakala
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
            nklR.message="Les informations iiif de l'image"
            try:
                # on converti l'objet json retournée en dictionnaire python
                nklR.dictVals = json.loads(response.text)
            except:
                pass
            
            # on retourne l'objet NklResponse maintenant entièrement rempli
            return nklR
        
        else:
            
            try:
                dicError = json.loads(response.text)
                nklR.message=dicError['message']
            except:
                pass

        
    except requests.exceptions.RequestException as e:
        nklR.code=-1
        nklR.message=e
        
    #on retourne l'objet NklResponse avec erreur (de nakala ou de connexion reseau)
    return nklR