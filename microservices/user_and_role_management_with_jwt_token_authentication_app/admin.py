from django.contrib import admin
from .user_and_role_management_models import Permission, User, Role
# Register your models here.

admin.site.register(Permission)
admin.site.register(User)
admin.site.register(Role)