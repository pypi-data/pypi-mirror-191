# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 15:50:10 2021

@author: Michael Nauge (Université de Poitiers)
"""

import requests
import json

from NklResponse import NklResponse


def get_users_me(nklTarget):
    """
    Récupération des informations sur l'utilisateur courant
    Retourne l'ensemble des informations disponibles sur l'utilisateur courant
        
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
    
    url = nklTarget.API_URL+"/users/me"
   
    
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
            nklR.message="Informations sur l'utilisateur courant"
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


 
 