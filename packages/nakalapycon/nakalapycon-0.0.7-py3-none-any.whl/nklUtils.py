# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 11:46:33 2021

@author: Michael Nauge (Université de Poitiers)
"""
import sys

import NklTarget as nklT
import nklAPI_Datas as nklD
import nklAPI_Collections as nklC


def delete_datas_uploads_all(nklTarget):
    """
    Permet de supprimer tous les fichiers présent dans l'espace temporaire
        
    Parameters
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test

    Returns
    -------
    List(NklResponse) : List(OBJ)
        une liste contenant des instances d'objet NklResponse
        - en cas de problème reseau ou de message d'erreur du serveur nakala
        l'objet NklResponse.isSuccess=False et le détails de l'erreur en version textuel
        sera dans NklResponse.message
        
        - en cas de réussite de la requete
        l'objet NklResponse.isSuccess=True et 
        pusiqu'il n'y a pas de retour json en cas de réussite 
        NklResponse.dictVals = {}

        
    """
    
    # on récupère la list des sha1 des fichiers de l'espace temporaire
    r = nklD.get_datas_uploads(nklTarget)
    
    listNklR = []
    
    for dicFile in r.dictVals:
        
        fileIdentifier = dicFile['sha1']
        
        #print("lancer suppression de", fileIdentifier) 
        rd = nklD.delete_datas_uploads(nklTarget, fileIdentifier)
        listNklR.append(rd)
        
    return listNklR
    

def put_collections_datas_rights(nklTarget, collectionId, userGroupId, role, checkOnly=True):
    """
    Permet d'ajouter des droits à un utilisateur ou un group d'utilisateur
    des droits (role) à toutes les datas d'une collection cible
    
    Pour currentData in listDesDatasDeLacollection:
        doi =  obtenir le DOI de la currentData
        
        si la data possède déjà le userGroupId avec le bon role
            pas besoin de modifier cette data
        
        sinon
            ajouter le userGroupId avec le bon role
    

    Parameters
    ----------
    nklTarget : OBJ
    	une instance d'un objet NklTarget permettant de choisir nakala_prod ou nakala_test
        
    collectionId : STR
        un COLLECTION identifier nakala.

    userGroupId : STR
        un USER ou USERGROUP identifier nakala.
        
    role : STR
        valeurs possibles :
            administrateur (ROLE_ADMIN) : consultation, modification, suppression, partage des droits de la collection
            éditeur (ROLE_EDITOR) : consultation, modification de la collection
            lecteur (ROLE_READER) : consultation de la collection même si elle est privée
            
    checkOnly : BOOL
        permet simplement de faire des affichage sans envoyer réellement les 
        requêtes d'ajouts de droit


    Returns
    -------

    NklResponse : List(OBJ)
        une liste d'objets NklResponse (un objet NklResponse par datade la collection cible)
        - en cas de problème reseau ou de message d'erreur du serveur nakala
        l'objet NklResponse.isSuccess=False et le détails de l'erreur en version textuel
        sera dans NklResponse.message
        
        - en cas de réussite de la requete
        l'objet NklResponse.isSuccess=True et 
        les métadonnées reçu seront dans
        NklResponse.dictVals : un dictionnaire contenant les metacollections obtenus depuis la reponse json du server


    """
    
    indexPage = 1
    lastPage = sys.maxsize
    
    listResponses = []
    
    while indexPage <= lastPage:
        rc = nklC.get_collections_datas(nklTarget, collectionId, page=indexPage, limit=1)
        indexPage+=1
        
        if rc.isSuccess:
            lastPage = rc.dictVals['lastPage']
            
            for currentData in rc.dictVals['data']:
                #obtenir le DOI de la current data
                doi = currentData['identifier']
                print("data Identifier:", doi)
                
                # verifier les rights existans de la data
                rd = nklD.get_datas_rights(nklTarget, doi)
                
                needAddRights = True
                
                if rd.isSuccess:
                    #print(rd.dictVals)
                    for right in rd.dictVals:
                        print(right['name'],right['role'])
                        
                        # verifie si le right actuel est celui attendu
                        if (userGroupId == right['id']) & (role == right['role']):
                            needAddRights = False
                            
                    # si on pas pas trouvé le rights attendu pour le usergroup cible
                    # il faut l'ajouter
                    if needAddRights:
                        print(">> add rights needed")
                        
                        if checkOnly==False:
                            print(">> >> send post_datas_rights request")
                            listDicRights=[{"id": userGroupId,"role": role}]
                            rr = nklD.post_datas_rights(nklTarget, doi, listDicRights)
                            listResponses.append(rr)
                    else:
                        print(">> do not need add rights")
                    
        else:
            listResponses.append(rc)
            lastPage = 0
            
            
    return listResponses
            


def isFileNameInData(nklResp, filename):
    """
    vérifier la présence d'un name dans les files d'une data nakala
    probablement un jour obsolete si ajout de cette interrogation dans l'api nakala
    
    Parameters
    ----------
    nklResp : OBJ nklResponse
        un Objet nklResponse (généralement obtenu par un appel à get_search_datas)
        on traite ici le cas particulier où il y a une seule data dans nklResponse
        

    Returns
    -------
    isFile : Bool
        retourne True si le filename est présent dans la data obtenu dans le nklRespone
        False sinon
    shaA : STR
        retourne le sha1 (que dans le cas où isFile==True)

    """
            
    data  = nklResp.dictVals
    
    if "files" in data:
        for file in data["files"]:
            if file["name"]==filename:
                return True, file['sha1']

    
    else:
        pass
    
    return False,""

    
def isFileSha1InData(nklResp, sha1):
    """
    vérifier la présence d'un sha1 dans les files d'une data nakala
    probablement un jour obsolete si ajout de cette interrogation dans l'api nakala
    
    Parameters
    ----------
    nklResp : OBJ nklResponse
        un Objet nklResponse (généralement obtenu par un appel à get_search_datas)
        on traite ici lecas particulier où il y a une seule data dans nklResponse
        

    Returns
    -------
    isFile : Bool
        retourne True si le filename est présent dans la data obtenu dans le nklRespone
        False sinon

    """
            
    data  = nklResp.dictVals
        
    if "files" in data:
        for file in data["files"]:
            if file["sha1"]==sha1:
                return True, file['sha1']
    
    else:
        return False, "" 
    
    
def isFileNameInUploads(nklResp, filename):
    """
    vérifier la présence d'un filename dans la liste des fichier "temporaire" uploads sur nakala avant agrégation par une data
    probablement un jour obsolete si ajout de cette interrogation dans l'api nakala
    
    Parameters
    ----------
    nklResp : OBJ nklResponse
        un Objet nklResponse (généralement obtenu par un appel à get_datas_uploads)
        

    Returns
    -------
    isFile : Bool
        retourne un tuple True + le sha1 si le filename est présent dans la data obtenu dans le nklRespone 
        sinon retourne False + empty string

    """
    
    listDico = nklResp.dictVals
    
    for kv in listDico:
        if kv['name']==filename:
            return True, kv['sha1']
    else:
        return False, ""
        
        

def isFileSha1InUploads(nklResp, filename):
    """
    vérifier la présence d'un sha1 dans la liste des fichier "temporaire" uploads sur nakala avant agrégation par une data
    probablement un jour obsolete si ajout de cette interrogation dans l'api nakala
    
    Parameters
    ----------
    nklResp : OBJ nklResponse
        un Objet nklResponse (généralement obtenu par un appel à get_datas_uploads)
        

    Returns
    -------
    isFile : Bool
        retourne True si le filename est présent dans la data obtenu dans le nklRespone
        False sinon

    """
    
    listDico = nklResp.dictVals
    
    for kv in listDico:
        if kv['sha1']==filename:
            return True
    else:
        return False
            
    