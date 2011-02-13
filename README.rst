Valentunes Docs
===============

(some blurb about what Valentunes is)
Eventually this app will be hosted at http://valentun.es.

Valentunes components
---------------------

1) Web input & mobile
    - Name
    - Interests
    - Intro note
    - Your email
2) Get suggested tracks 
    - from Musixmatch 
    - and/or from Hunch (based on your sweetheart's Twitter / Facebook ID)
3) From this list of tracks, display filtered playlist using Echonest API
    - by genre
    - by energy
    - by likeness to a favorite artist
    - by ...?
4) "The Gift" - present the greeting and song at a unique URL
5) Bonus: send "valentune" to your sweetheart by phone using Twilio
    - add an optional personal recorded greeting via Twilio

Getting started
---------------

You must install the components using pip::

    $ git clone https://github.com/natea/valentunes.git
    $ virtualenv valentunes
    $ cd valentunes
    $ source bin/activate
    $ easy_install pip
    $ pip install -r requirements.txt
    
Now you can start up Django with::

    $ cd vt
    $ ./manage.py runserver
    
Testing with curl
-----------------

To add a new card via the API, type this command in the terminal::

    $ curl localhost:8000/api/ -F "from_name=Nate" -F "from_email=nate@valentun.es"
    {
        "interests": "", 
        "to_email": "", 
        "from_name": "Josh", 
        "create_date": "2011-02-12 18:25:45", 
        "intro_note": "", 
        "_state": "<django.db.models.base.ModelState object at 0x1019b2910>", 
        "to_phone": "", 
        "from_email": "nate@valentun.es", 
        "to_name": "", 
        "from_phone": "", 
        "id": 3
    }
    
Now fetch that record you just created::

    $ curl localhost:8000/api/3/
    {
        "interests": "", 
        "to_email": "", 
        "from_name": "Nate", 
        "create_date": "2011-02-12 18:25:45", 
        "intro_note": "", 
        "_state": "<django.db.models.base.ModelState object at 0x1019b2c90>", 
        "to_phone": "", 
        "from_email": "nate@valentun.es", 
        "to_name": "", 
        "from_phone": "", 
        "id": 3

If you want to delete the record, type this command::

    $ curl-X DELETE http://localhost:8000/api/1/

API resources
-------------

    * `Example of django-piston <https://github.com/pelme/todos_django_piston/>`_
    * `Example with OAuth <https://github.com/clemesha/django-piston-oauth-example/>`_
    * `Presentation of django-piston <https://bitbucket.org/Josh/django-piston-presentation/>`_