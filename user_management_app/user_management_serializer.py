from rest_framework import serializers 
from user_registeration.models import UserRegisterationModel
from django.contrib.auth.models import User

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = (
            'username',
            'email',
            'password'
        )

class UserRegisterationModelSerializer(serializers.ModelSerializer):
    class Meta :
        model = UserRegisterationModel
        exclude = (
        'user',
        'profile_picture',
        'resume',
        'pan_card',
        'adhar_card')

class UserRegisterationModelFileSerializer(serializers.ModelSerializer):
    class Meta : 
        model = UserRegisterationModel
        fields = (
            'profile_picture',
            'resume',
            'pan_card',
            'adhar_card'
        )

class DatatableSerializer(serializers.ModelSerializer):
    class Meta :
        model = UserRegisterationModel
        fields = (
            'profile_picture',
            'user_name',
            'email',
            'resume',
            'pan_card',
            'adhar_card',
            'user_id'
        )