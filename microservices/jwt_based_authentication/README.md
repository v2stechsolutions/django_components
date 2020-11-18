# JWT based user authentication

This app helps you to authenticate user using JWT


## Installation

Install simple JWT package using pip

```bash
pip install djangorestframework-simplejwt
```

Copy and paste this app to your project

Add this app under INSTALLED_APPS section in settings.py

Then, In settings.py add rest_framework_simplejwt.authentication.JWTAuthentication to the list of authentication classes.

```bash
REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework_simplejwt.authentication.JWTAuthentication',
  ),
}
```

## Usage

```bash
/jwt/access_token/
```
Takes a set of user credentials and returns an access and refresh JSON web


Parameters

username
password

You can use the access token to prove authentication for a protected view


When access token expires you can use refresh token to get access token

```bash
/jwt/refresh_token/
```
Takes a refresh type JSON web token and returns an access type JSON web

