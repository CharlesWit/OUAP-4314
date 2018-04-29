
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
How to launch the project
=========================

You may first need to pull the Docker image for MongoDB from dockerhub:

.. code-block:: bash

    docker pull mongo

Navigate to OUAP-4314/Evaluation/Projet and start the containers:

.. code-block:: bash

    docker-compose up

You can also start the containers in detached mode and check their logs in real time:

.. code-block:: bash

    docker-compose up -d
    docker-compose logs -f

Check if the containers are up:

.. code-block:: bash

    docker-compose ps

Gracefully shut the containers down:

.. code-block:: bash

    docker-compose down

Deploy the project on macOS:

.. code-block:: bash

    docker-compose -f mac_docker-compose.yml up
