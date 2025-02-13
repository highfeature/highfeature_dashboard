# Highfeature Dashboard
![Preview of Highfeature Dashboard](https://github.com/highfeature/highfeature_dashboard/blob/main/docs/images/demo.png)

POC (Just for fun) of a dashboard made with Django 5+ (backend part) and HTMX (Frontend part). The application does not have the ambition to replace a Dashy or a Kubernete dashboard, I do it just for fun and to show Django can does it, if needed.

NOTE: this POC is WIP, it uses Redis and Celery as quick task manager, it will be containerized to make an easy management.
The main features for now are:
- like Dashy, it accept a config in yaml
- multiple type of component displayed by groups
- display working status, and last time see up

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT License

**Special THANKS to all contributors of all open source framework and library used in that POC.**

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ ./manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy highfeature_dashboard

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery
Twist:
Celery works with Redis.
Redis Server listens to the client and enqueues the task to the task queue. 
In simple words, Django and Celery use Redis to communicate with each other. 
It means we have to install Redis as well to make our celery work perfectly fine.

This app comes with Celery.

To run a celery worker:

```bash
cd highfeature_dashboard
export CELERY_BROKER_URL=
export USE_DOCKER=yes
celery -A config.celery_app worker -l info
```

Please note: 
For Celery's import magic to work, it is important _where_ the celery commands are run. 
If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. 
You can start it as a standalone process:
```bash
cd highfeature_dashboard
celery -A config.celery_app beat -l info
```

or you can embed the beat service inside a worker with the `-B` option 
(not recommended for production use):
```bash
cd highfeature_dashboard
celery -A config.celery_app worker -B -l info
```
Then run or debug the app in Pycharm or other.

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at 
<https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with 
the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

## Run locally
Create a file .envs/.local/.django containing
```commandline
# General
# ------------------------------------------------------------------------------
USE_DOCKER=yes
IPYTHONDIR=/app/.ipython
# Redis
# ------------------------------------------------------------------------------
REDIS_URL=redis://redis:6379/0

# Celery
# ------------------------------------------------------------------------------
CELERY_BROKER_URL=

# Flower
CELERY_FLOWER_USER=<your-celery-flower-complex-username>
CELERY_FLOWER_PASSWORD=<your-celery-flower-complex-and-long-password>
```
Create a file .envs/.local/.postgres (if you use Postgres, right now sqlite3 is used for the POC) containing
```commandline
# PostgreSQL
# ------------------------------------------------------------------------------
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=highfeature_dashboard
POSTGRES_USER=<your-postgres-complex-username>
POSTGRES_PASSWORD=<your-postgres-complex-and-long-password>

# Sqlite3 (NEVER IN PRODUCTION)
DATABASE_URL=db.sqlite3
```
```shell
source .envs/.local/.django
source .envs/.local/.postgres
source your-virtual-env/bin/activate
python ./manage.py
```
Administrative tasks:
```shell
source ~/venv/p310_djangohtmx/bin/activate
export DJANGO_SETTINGS_MODULE=config.settings.local
export DATABASE_URL=db.sqlite3
python ./manage.py makemigrations
python ./manage.py createsuperuser
python ./manage.py migrate
```

## Run in Production
Create a file .envs/.production/.django containing and
create a file .envs/.production/.postgress containing
```commandline
No, I'm kidding, NEVER put into production a product that is not tested, 
that has not passed all validation tests, in DEV and UAT environment, 
and whose deployment process is not automated, and I DON'T kid on that.
And has you can see, put all secret in vault or in worse case in files,
that are never store in the repository.
Have a nice days.
```
