# USER AND ROLE MANAGEMENT WITH JWT TOKEN AUTHENTICATION

This app helps you to to add users and roles in your project with jwt authentication token

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
token/
```
Takes a set of user credentials and returns an access and refresh JSON web


Parameters

username
password

You can use the access token to prove authentication for a protected view

When access token expires you can use refresh token to get access token


```bash
token/refresh
```
Takes a refresh type JSON web token and returns an access type JSON web



```bash
/user
```
No parameter required

Get all the user list from database


```bash
/role
```
No parameter required

Get all the role list from database


```bash
/user/{id}
```
Parameter required

User id

GET, PUT and DELETE methods can be used to get, update and delete data respectively


```bash
/role/{id}
```
Parameter required

Role id

GET, PUT and DELETE methods can be used to get, update and delete data respectively
