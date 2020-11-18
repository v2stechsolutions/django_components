from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from .models import WordTemplate

class WordTemplateSerializer(serializers.ModelSerializer):
    class Meta :
        model = WordTemplate
        fields = "__all__"
