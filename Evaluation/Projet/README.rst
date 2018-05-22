
=========================
Projet - Sujet 2
=========================

Objectif : Construire une base MongoDB des jardins et musées parisiens consultable via une interface Flask
URLs : https://meslieux.paris.fr/principaux-parcs-et-jardins, https://meslieux.paris.fr/musees-municipaux
Structure de la base MongoDB :

.. code-block::

    <adresse>:
        {   "numero" : [<32-bit integer>] ,
            "voie" : <String>,
            "nom_voie" : <String>,
            "code_postal" : <32-bit integer>,
            "ville" : <String> }

    <loc>:
        {   "lat" : <Double>,
            "lon" : <Double>
        }

    <station> :
        {   nom:<String>,
            adresse:<adresse>
        }

    <metro> : <station>
    <bus> : <station>
    <velib> : <station>

    <horaire> :
        {
            <jour> : <String>,
            <heures> : [<32-bit integer>, <32-bit integer>] # 7:00 - 21:00 stored as [ 420, 1260]
        }

    <tarif> :
        {
            "categorie" : <String>,
            "prix" : <Double>
        }


    { "appellation" : <String>,
        "adresses" : [<adresse>],
        "locs" : [<loc>],
        "metros" : [<metro>]
        "buss" : [<bus>]
        "velibs" : [<velib>]
        "infos" : <String>,
        "horaires" : [<horaire>],
        "tarifs" : [tarif]
    }

Exemple : http://equipement.paris.fr/musee-cognacq-jay-1519, http://equipement.paris.fr/jardin-des-tuileries-1795
Ressources externes : on pourra utiliser https://adresse.data.gouv.fr/api pour le geocoding

=========================
Lancer le projet
=========================

**TEMPORAIRE**

Lancer un serveur mongodb :

.. code-block:: bash

    mongod -dbpath ~/data/

Dans une nouvelle fenêtre de terminal, se placer dans le dossier OUAP-4314/Evaluation/Projet, puis taper les commandes qui suivent :

.. code-block:: bash

    python3 ./soup/AddDatabase.py

et dans une (encore) nouvelle fenêtre :

.. code-block:: bahs

    python3 ./flask/run.py

Dans un navigateur web, accéder à la base des musées via l'url http://localhost:5000/musees, et à celle des jardins via http://localhost:5000/jardins

=========================

Avant tout, assurez-vous d'avoir récupéré l'image Docker pour MongoDB depuis le dockerhub :

.. code-block:: bash

    docker pull mongo

Placez-vous dans le dossier OUAP-4314/Evaluation/Projet, puis lancer les containers :

.. code-block:: bash

    docker-compose up

Si les containers ont bien été lancés, vous devriez les voir listés à l'exécution de cette commande :

.. code-block:: bash

    docker-compose ps

Pour arrêter les containers sans risques, utilisez la commande suivante :

.. code-block:: bash

    docker-compose down
