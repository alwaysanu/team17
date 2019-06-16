# Team17

## Requirements
1. Django version - 2.15
2. Python version - 3.7
3. Python Packages  
    * graphene-django
    * graphene
    * webpreview
    * Google-Search-API

To install all the packages required for the project use `requirements.txt` file. To install packages using `requirements.txt` run on terminal:
```sh
pip install -r requirements.txt
```

## Database

We are using SQLite as our database. To create database `cd` into  project root and run on terminal:
```sh
python manage.py makemigrations
python manage.py migrate
```

## Running Server
Head to terminal and run

```sh
python manage.py runserver
```
The server will be running on `localhost:8000`

## APIs Used

1. GraphQL
2. BoredAPI
3. Google-Custom-Search-API
