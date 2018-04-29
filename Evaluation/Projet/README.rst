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
