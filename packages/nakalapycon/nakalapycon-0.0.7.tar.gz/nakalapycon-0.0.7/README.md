# NakalaPycon

Librairie Python pour interagir avec Nakala (Nakala : entrepôt de données de recherche en SHS développé par Huma-Num).

Cette librairie vise à simplifier l'utilisation de l'[API Nakala](https://apitest.nakala.fr/doc) depuis les programme écrits en Python.

Elle peut être vue comme un *wrapper* de l'API.
Les différents end-points de l'API sont séparées dans les fichiers python suivants :
- [nklAPI_Datas](nakalapycon/src/nklAPI_Datas.py)

- [nklAPI_Collections](nakalapycon/src/nklAPI_Collections.py)

- [nklAPI_Groups](nakalapycon/src/nklAPI_Groups.py)

- [nklAPI_Users](nakalapycon/src/nklAPI_Users.py)

- [nklAPI_Vocabularies](nakalapycon/src/nklAPI_Vocabularies.py)


Pour mieux comprendre le fonctionnement sous-jacent de cette librairie nous recommandons les lectures suivantes :
- [NakalaPyConnect : Dépôt facilitant l'appropriation de Nakala et de son API.](https://gitlab.huma-num.fr/mnauge/nakalapyconnect)
- [Notebook Api Nakala : Une présentation de l'API de NAKALA sous forme d'un notebook Jupyter](https://gitlab.huma-num.fr/huma-num-public/notebook-api-nakala)

## Buts

## 1. Nakala Production versus Nakala Test
L'entrepôt Nakala existe sous 2 instances :
- (Nakala Test)[https://test.nakala.fr/]
- (Nakala Production)[https://nakala.fr/]

Lors de développements en interactions avec Nakala, il est impératif de commencer par prototyper sur Nakala Test avant de lancer ses scripts sur Nakala Production. 

Pour faciliter le choix et le changement de Nakala Test vers Nakala Production, la librairie **nakalapycon** propose une classe [NklTarget](nakalapycon/src/NklTarget.py) dont on créer une instance la manière suivante
```python
# création d'une cible Nakala Test avec une Key Api d'utilisateur valide
myApiKey = "f41f5957-d396-3bb9-ce35-a4692773f636"
targetTest = nklT.NklTarget(isNakalaProd=False, apiKey=)


# création d'une cible Nakala Production avec une Key Api d'utilisateur vide
myApiKey = ""
targetProd = nklT.NklTarget(isNakalaProd=True, apiKey=)
```

Toutes les fonctions mise à dispositions dans **nakalapycon** prennent en paramètre entrant une instance d'un objet **NklTarget**. Par ce mécanisme
il est très facile de changer le Nakala ciblé.
Il est même facilement envisageable de réaliser des communications entre Nakala Test et Nakala Production.


### 2. Unifier les valeurs retours 
Lorsque l'on communique avec l'API Nakala il est important de pouvoir obtenir les objets JSON contenant les données retournés par le server mais il est également important de savoir si la requête c'est réalisée correctement. Cependant, les codes retours serveurs sont assez différents d'un access-point à l'autre. Tandis qu'il est en général simplement important de savoir si la requête s'est passée correctement Oui ou Non ?
Pour cela, toutes les fonctions de **nakalapycon** retourne une instance d'un objet [NklResponse](nakalapycon/src/NklResponse.py)

La classe **NklResponse** peut être vue comme un sac contenant 4 variables :

- NklResponse.isSuccess : retourne False en cas de code d'erreur server ou cas de problème reseau

- NklResponse.code : le status_code retourné par le serveur Nakala

- NklResponse.message : la description associée au code d'erreur nakala ou le message d'exception de la librairie request

- NklResponse.dictVals : les valeurs json renvoyés par le serveur en cas de succès sous la forme d'un dictionnaire python



### 3. Encapsuler les appels bas niveau nécessaires au requêtage HTTP de l'API Nakala.

Cette librairie se charge d'encapsuler et masquer les appels bas niveau à la libraire [request](https://docs.python-requests.org/en/latest/) nécessaires au requetage HTTP de l'API Nakala et de traiter les codes retours servers.

Lors de la communication avec l'API Nakala, il peut se produire 2 types d'erreurs classiques :
- les erreurs retournées par le server Nakala 
    - en cas de requêtes mal formées 
    - en cas de mauvaises valeurs : comme c'est le cas lorsque l'on cherche à modifier une DATA Nakala alors que nous ne disposons pas des droits suffisants sur cette DATA.
- les erreurs du au réseau internet
    - lorsque notre connexion wifi se coupe
    - lorsque le proxy de notre établissement disfonctionne
    - lorsque le serveur nakala est momentanement inacessible
    
Afin de décharger les développeurs de script communiquant avec Nakala de traiter la difficulté de ces deux types d'erreurs dont les erreurs réseaux levant des "exceptions" provoquant l'arrêt du script si elles ne sont pas capturées, la librairie **nakalapycon** prend en charge la capture de toutes erreurs et retourne de manière unifiée des **NklResponse**.

### 4. Faciliter le développement de fonctions plus aux niveaux
En ayant simplifier l'accessibilité de l'API il est plus facile d'envisager la création de fonctions plus haut niveaux. Comme par exemple des traitements par lots sur toutes les DATA d'un COLLECTION.

Ce genre de traitement haut niveau se trouve dans [nklUtils](nakalapycon/src/nklUtils.py)




## Cas d'usages

### 1. Intéragir avec Nakala depuis un notebook Jupyter

- Générer un rapport de donnnées intéractif en ciblant une collection depuis un notebook jupyter.

- Ajouter des droits administrateurs à un groupe d'utilisateur sur toutes les DATA d'une COLLECTION


### 2. Développer sa chaîne de traitement semi-automatisé intégrant Nakala dans la chaîne

- Fabriquer son outil de dépôt et MAJ "sur-mesure" intégrant Nakala. Découvrir le projet [sync Sharedocs Nakala](https://gitlab.huma-num.fr/mshs-poitiers/plateforme/syncsharedocsnakala)

## Installation



Cette librairie est déposée sur l'entrpôt de package [PyPi](https://pypi.org/project/nakalapycon/).

Il suffit donc de l'installer avec la commande :
```
pip install nakalapycon
```

puis de l'utiliser depuis votre script après un import :

```
import nakalapycon as nklco

```

Il est également possible de l'installer depuis Anaconda.Navigator




