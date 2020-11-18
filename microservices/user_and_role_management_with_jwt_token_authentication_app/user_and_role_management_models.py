from django.db import models

class Role(models.Model):
    predefine_roles = models.CharField(max_length=20, blank=False, default='', unique=True)

class Permission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE,null=True)
    add_user = models.BooleanField(default=False)
    edit_user = models.BooleanField(default=False)
    delete_user = models.BooleanField(default=False)
    add_role = models.BooleanField(default=False)
    edit_role = models.BooleanField(default=False)
    delete_role = models.BooleanField(default=False)

class User(models.Model):
    username = models.CharField(max_length=70, blank=False, default='', unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=200, blank=False, default='')
    last_name = models.CharField(max_length=200, blank=False, default='')
    email = models.EmailField(max_length=200, blank=False, default = '')
    password = models.CharField(max_length=20, blank=False, default= '')
    