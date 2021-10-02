Castle Dice `Revamped`
======================

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

:License: MIT

I started this project many years ago, back in the days when python 3 was less popular, and I was
less experienced.  I've been thinking about it recently, and decided to start from scratch, as many
pieces were tangled and confusing, and severely lacking tests.

Welcome to the revamp - an exclusively python 3 endeavor to convert one of my favorite board games,
**Castle Dice**, into a multi-player web application built in Django.  This is a labor of love and
has no definite end date in mind.  Merely a constant attempt to one day reach the finish line...

The below instructions will change and be updated as this project is transitioned.  I do not
promise their accuracy nor their usability.  Chunks will be updated piece-meal as I get to them.

CastleDice Project
--------------------

This repo is my attempt to convert a beloved board game into a multi-player web app using Django.

This has been a labor of love for many years, and has been very slow going.  Not all pieces are built-out and many pieces are not yet functional at all.

Regardless, this is my excuse to delve deep into understanding game mechanics, Django, and melding the two together.  It IS NOT meant to be a replacement for owning the game.  I started this out of a _love_ for the game after playing it many, _many_ times.  It is also my hope that I will one day be able to play it simultaneously with my friends who live out of state and don't visit as often.

With that in mind, this repo exists as a `proof of concept`.  Please do not use it as best practices or an excuse to play the game without buying.  It is likely that this repo will no longer be public if/when if acheives a fully functional state.

I love **Castle Dice** and the `Fun to 11 <http://funto11.com/>`_ game company.  I think I own all of their games and expansions.  Please support them directly!


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Setup Docker
------------

See the instructions at `Cookiecutter Django`_ or the local version `README-docker.rst`.

.. _`Cookiecutter Django`: https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy castledice

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html

Deployment
----------

The following details how to deploy this application.

Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
