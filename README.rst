============
qlutter_todo
============

qlutter_todo is a relatively small API for todo management. It's build with Flask, Flask-Restful, marshmallow and a few other packages.

Install for development
=======================

You can run qlutter_todo locally in two ways. Either like a traditional python project, or using docker & docker-compose.


Standard setup
--------------

Using your preferred env manager (ex. virtualenv) get the dependencies with pip.

::

    pip install -r requirements.txt


Add this project's directory to the PYTHONPATH.

::

    export PYTHONPATH=$PYTHONPATH:$(pwd)


To run the API use the following command.

::

    python qlutter_todo/app.py 


Docker-compose setup
--------------------

Docker-compose will prepare the docker image and start a container with the API with the following.

::

    docker-compose up


Configuration
=============

Configuration can be found in ``qlutter_todo/application.cfg``. For further reference regarding available options see the following websites.

- http://flask.pocoo.org/docs/0.10/config/#builtin-configuration-values
- https://pythonhosted.org/Flask-JWT/#configuration-options


Testing
=======

You can execute the test suite using the command:

::

    py.test


API Documentation
=================

The API is documented using the OpenAPI specification. Make sure ``SWAGGER = True`` in the ``application.cfg``.
With the API running, visit http://your_api_domain/static/index.html?url=/spec

License
-------

MIT licensed. See the `LICENSE <https://github.com/sloria/webargs/blob/dev/LICENSE>`_ file for more details.
