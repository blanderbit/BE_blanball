# Architecture of the repository

This is a short overview of the general architecture and structure of the repository, to help you orient yourself.

## `project/` - Project root folder

Contains all the main application modules

- api_keys - it is intended for site administration. Creating, deleting api keys, access rights by keys, etc.
- authentication - it is intended for user interaction with the application. Registration, authorization, profile view, password change, etc.
- bugs - it is intended to leave feedback from users and detect app bugs
- cities - it is intended to work with a map, coordinates, cities, etc.
- events - it is intended for user interaction with the event. Creating an event, deleting an event, entering an event, etc
- notifications - it is intended for user interaction with notifications and sending notifications. Viewing notifications, deleting, reading, etc. This application is also responsible for working with the current version and the state of those works.
- reviews - is it intended for user interaction with reviews. Get my reviews, leave a review for a user, an event, etc.

## `project/settings` - All project settings

- /components/celery.py - celery framework settings.
- /components/core.py - the main settings file, all applications and configs are connected there.
- /components/smtp.py - google smtp settings file.
- /components/storages.py - project storages settings. 

    * PostgreSQL - database 
    * Redis - temporary data store
    * MinioStorage - images storage

- /components/valiables.py - the file that contains all the basic constants and settings variables.


## `project/templates` - All project html templates

Contains html templates, in particular templates for sending by mail

## `project/static` - All project static files

contains all the static files of the project. In particular css and js. 
Files are placed in this folder when executing the command python manage.py collectstatic

## `changelog/` - Project changelog

Contains update history files, each file is a specific version of the application

## `nginx/` - Web server and proxy

Contains the configuration of the web server and Nginx proxy

## `scripts/` - Scripts for launching utilities

It contains all possible bash and not only scripts. Mainly used to run containers and other utilities

## `.github/workflows/` - Continuous Integration and Deployment

Contains Continuous-integration (CI) workflows, run on commits/PRs to the GitHub repository.

## Parent theme - `pydata-sphinx-theme`