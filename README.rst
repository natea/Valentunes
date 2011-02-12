Valentunes components
=====================

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
===============

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
    
API resources
=============

Example code: https://github.com/pelme/todos_django_piston/