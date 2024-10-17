## DjangoRestFramework Simple Blog

A simple blog project with django rest framework

## Usage
- Clone Project From Git
- Run ```cd drf```
- Run ```python -m venv venv```
- In Windows: Run ```venv\Scripts\activate```
- In (Linux and mac os): Run ```source venv/bin/activate```
- Run ```pip install -r requirements.txt```
- Run ```python manage.py makemigrations```
- Run ```python manage.py migrate```
- Run ```python manage.py runserver```


I used sqlite db in this project. You can use any databases like (Mysql, Postgres) and put your db info in ```core/settings.py```


## How to create superuser?
####In Windows:
Run ```venv\Scripts\activate```
Run ```python manage.py createsuperuser```
Enter your name, email and password

####In (Linux and mac os):
Run ```source venv/bin/activate```
Run ```python manage.py createsuperuser```


## License
Copyright © 2011-present, [Encode OSS Ltd](https://www.encode.io/). All rights reserved.
