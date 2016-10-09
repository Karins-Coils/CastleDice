# CastleDice Project

This repo is my attempt to convert a beloved board game into a multi-player web app using Django.

This has been a labor of love for many years, and has been very slow going.  Not all pieces are built-out and many pieces are not yet functional at all.

Regardless, this is my excuse to delve deep into understanding game mechanics, Django, and melding the two together.  It IS NOT meant to be a replacement for owning the game.  I started this out of a _love_ for the game after playing it many, _many_ times.  It is also my hope that I will one day be able to play it simultaneously with my friends who live out of state and don't visit as often.

With that in mind, this repo exists as a _proof of concept_.  Please do not use it as best practices or an excuse to play the game without buying.  It is likely that this repo will no longer be public if/when if acheives a fully functional state.

I love **Castle Dice** and the **Fun to 11** game company.  I think I own all of their games and expansions.  Please support them directly!

# Developer Instructions

Hopefully in the future, I will commit a vagrantfile and setup for this project.  Until then, a pip requirements file is considered the best quickstart.

This code is written and tested for use with **Python3**.

## Environment Setup

If on Mac, install and start Postgres.app, and add `:/Applications/Postgres.app/Contents/Versions/latest/bin` to PATH

I recommend virtualenv or virtualenvwrapper.
```
virtualenv --python=python3 venv
```

Then activate your virtualenv

```
source venv/bin/activate
```

Install the package requirements

```
pip install -r requirements/local.txt
```

Copy the example environment settings.  Be sure to remove the "DATABASE_URL" line.

```
cp CastleDice/config/settings/.django-env-example.json CastleDice/config/settings/.django-env.json 
```

Generate a shiny new Django Secret Key, and put it in the `.django-env.json` you just created

```
python -c "from django.utils.crypto import get_random_string; print get_random_string(50, 'abcdefghijklmnopqrstuvwxyz0123456789\!@#$%^&*(-_=+)')"
```

## Database Setup

If you installed the Postgres.app, you should have access to the following commands.  Use them to create the database and the user.  Type 'admin' into the password prompt when asked. This matches what we've listed in `CastleDice/config/settings/local.py`

```
createdb CastleDice
createuser -s -W admin
```

You then need to create all the needed tables in the database. From inside the `CastleDice` folder, run:

```
python manage.py migrate
```

Create a django superuser

```
python manage.py createsuperuser
```

## Start your server

From inside the `CastleDice` folder:

```
python manage.py runserver --settings config.settings.local
```

You can now access the website at `localhost:8000`
