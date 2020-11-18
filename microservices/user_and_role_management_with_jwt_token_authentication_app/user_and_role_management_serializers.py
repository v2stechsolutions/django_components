from rest_framework import serializers 
from .user_and_role_management_models import User, Role, Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta :
        model = Permission
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username', 
                  'role',
                  'first_name',
                  'last_name',
                  'email',
                  'password')
        
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"