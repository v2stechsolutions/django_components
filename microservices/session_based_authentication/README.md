# Session based user authentication

This app is used for session based user authentication, register a new user and forgot password apis


## Installation

Install simple JWT package using pip

```bash
pip install django-rest-auth
```

Copy and paste this app to your project

Add this app under INSTALLED_APPS section in settings.py

Add 'rest_auth' under INSTALLED_APPS section.

Then, In settings.py add EMAIL Configurations.

```bash
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
```

Migrate your database
```bash
python manage.py migrate
```

