# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 15:02:00 2021

@author: Michael Nauge (Université de Poitiers)
"""

class NklResponse:
    """
    Une classe (sac de variable) permettant la manipulation homogène 
    des responses serveurs renvoyées et communication reseau.
    On va faire en sorte d'éviter à l'utilisateur d'éviter une gestion d'exception et de message d'erreur
    a deux niveaux (serveur nakala et communication reseau avec request).
    
    """
    
    # le numéro de code renvoyé par le serveur nakala 
    # ou un numéro negatif en cas de problème réseau et/ou avec la librairie request
    code = 0
    # la description associée au code d'erreur nakala
    # ou une exception de la librairie request
    message = ""
    # les valeurs json renvoyés par le serveur en cas de succès sous la forme d'un dictionnaire python
    dictVals = {}
    # un boolean informant de la réussite de la requete
    # c'est pratique quand on sait qu'en fonction des requetes les codes de réussites sont différents
    # 200 pour un get réussi 
    # 204 en cas de modification réussi, 204 en cas de suppression réussie
    # 200 pour un post réussie
    # et aussi que des erreurs peuvent avoir lieux avant le serveur nakala
    # comme des problèmes reseaux ...
    # ça permet de simplifier/uniformiser les appels
    isSuccess = False

    def __init__(self, code=0, message="", dictVals={}, isSuccess=False):
        self.code=code
        self.message=message
        self.dictVals=dictVals
        self.isSuccess=isSuccess
        
        
    def __str__(self):
        return f'nklResponse isSuccess:{self.isSuccess}, code:{self.code},  message:{self.message},  dictVals:{self.dictVals}'
    
        
