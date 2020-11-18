# Caching using REDIS and Django Rest API

This app will be able to cache all the products, making it easy and fast to retrieve data is subseqquent queries


## Installation

Install redis using pip

```bash
pip install django-redis
```

Copy and paste this app to your project

Add this app under INSTALLED_APPS section in settings.py


## Usage


### Migrations

Create an initial migration for our product model and sync the database.


```bash
python manage.py makemigrations
python manage.py migrate
```

### Configuring Redis in Python Applications

Add the following lines to the settings.py

```bash
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```