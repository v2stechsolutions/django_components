from django.db import models

class Role(models.Model):
    predefine_roles = models.CharField(max_length=20, blank=False, default='', unique=True)

class User(models.Model):
    username = models.CharField(max_length=70, blank=False, default='', unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200, blank=False, default='')
    email = models.EmailField(max_length=200, blank=False, default = '')
    def __str__(self):
        return self.username