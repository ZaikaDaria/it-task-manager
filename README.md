# Task Manager!

## Django-based application

This task manager helps you to get organized your thinks and increase efficiency. This repo contains the CRUD (Create, Retrieve, Update, Delete) concept, with this concept you can create basic Django applications and understand how a few things work, like urls, views, models and so on. 

### Installation
* Clone the repo.
```git
git clone git@github.com:ZaikaDaria/it-task-manager.git
```
* Install packages with pip
```
pip install -r requirements.txt
```
* Create database (Django default is sqlite3)
```
python manage.py migrate
```
* Create superuser to use Django admin panel
```
python manage.py createsuperuser
```
* Run!
```
python manage.py runserver
```