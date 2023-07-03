# Task Manager!

## Django-based application

This task manager helps you to get organized your thinks and increase efficiency. This repo contains the CRUD (Create, Retrieve, Update, Delete) concept, with this concept you can create basic Django applications and understand how a few things work, like urls, views, models and so on. 

### Check it out!
[Task Manager deployed to Render] (https://task-manager-zrmc.onrender.com/)
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
### Environment Variables Configuration

**.env.example** file helps you to configue the environment variables for your project.

#### Usage
* Rename this file from **.env.example** to **.env**.
* Fill in the necessary values for the environment variables.

#### Variables
Here is a list of environment variables used in the application:
**SECRET_KEY:** the token, encrypting session data, signing cookies, and protecting against tampering or forgery attacks.

#### Notes
* Make sure to keep the .env file secure and do not share it publicly, as it may contain sensitive information.
* It is recommended to use a different set of environment variables for production, development, and testing environments.
* If you are using a different configuration management system (e.g., Docker Compose, Kubernetes ConfigMap), you may not need to use an .env file. Adjust the configuration according to your environment.

#### Test user
Please use credentials below to review the app opportunities
```
Login: test_user
Password: rttgd234_
```