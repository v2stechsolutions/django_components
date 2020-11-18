from rest_framework import serializers 
from .user_and_role_management_models import User, Role

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'username', 
                  'role',
                  'name',
                  'email')
        

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"