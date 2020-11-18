import datetime
import uuid
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import WordTemplateSerializer
from . import generate
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http.response import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_registeration.models import UserRegisterationModel
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.exceptions import InvalidToken
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import HTTP_HEADER_ENCODING, authentication
from user_registeration.models import (Language, PageName,
                                       PageLabel)

from .get_info_msg import set_session_language, get_info_messages

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['token_value'] = uuid.uuid4().hex
        cache.set(token['token_value'], user, timeout=CACHE_TTL)
        return token    

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])
        data = {'access': str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)
    
        return data  

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
    token_obtain_pair = TokenObtainPairView.as_view() 



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['token_value'] = uuid.uuid4().hex
        cache.set(token['token_value'], user, timeout=CACHE_TTL)
        return token


    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        data['id'] = self.user.id
        role = UserRegisterationModel.objects.filter(user_id=self.user.id).values('role')
        data['role_id'] = role[0]["role"]

        return data   


class CustomJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            header = "Bearer "+request.GET['token']
            header = header.encode(HTTP_HEADER_ENCODING)

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
    
        validated_token = self.get_validated_token(raw_token)
        payload = token_backend.decode(raw_token, verify=True)


        if payload['token_value'] in cache.keys("*"):
            return cache.get(payload['token_value']), validated_token
        else:
            raise InvalidToken()


    def get_header(self, request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        header= request.META.get('HTTP_AUTHORIZATION')
     
        if isinstance(header, str):
            # Work around django test client oddness
            header = header.encode(HTTP_HEADER_ENCODING)
        return header    


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()


class LoginView(APIView):
    """ Login page """
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    
    def get(self, request):
        """ get login page """

        get_language = set_session_language(request)
         
        try:
            return Response(template_name="user_authentication/login.html")     
             
        except Exception as e:
            
            print("exception while showing login page", e)
            info_message = get_info_messages(get_language, 'login_page_error')
            print("cannot get login page", info_message)
            return Response({"success": False, "error": str(info_message)})


class LogoutView(APIView):
    """ Logout class """
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        """ get login page """

        get_language = set_session_language(request)
        
        try:
            info_message = get_info_messages(get_language, 'logout_success')
            print('You have successfully logged out', info_message)
            return Response({'data': str(info_message)}, status=204, template_name="user_authentication/login.html")
        except Exception as e:
            print("exception while showing login page", e)
            info_message = get_info_messages(get_language, 'logout_error')
            print("User Cannot logout", info_message)
            return Response({"success": False, "error": str(info_message)})


class NewPasswordView(APIView):
    """ Get forgot passworrd page """
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        get_language = set_session_language(request)
        try:
            return render(request, 'user_authentication/forgot_password.html')
        except Exception as e:
            info_message = get_info_messages(get_language, 'password_page_error')
            print("exception while getting page", e)
            print("Cannot get reset password page", info_message)
            return Response({"success": False, "error": str(info_message)})
        

class Dashboard(APIView):
    """shhow active users and inactive users count on dashboard"""
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        """ active and inactive users count """
        
        get_language = set_session_language(request)
        try:
            print(request.GET['token'],"dashboard")
            today = datetime.date.today() + datetime.timedelta(days=1)
            last_week = datetime.date.today() - datetime.timedelta(days=7)
            new_users = User.objects.filter(last_login__isnull=True).filter(is_superuser=False).count()
            recently_looged_users = User.objects.filter(last_login__range=(last_week, today)).filter(is_superuser=False).count()
            active_users = new_users + recently_looged_users

            total = User.objects.filter(is_superuser=False).count()
            inactive_users = total - active_users

            return Response({'active': active_users, 'inactive': inactive_users}, template_name="user_authentication/dashboard.html")
        except Exception as e:
            print("exception in dashboard", e)
            info_message = get_info_messages(get_language, 'dashboard_error')
            print("Unable to get Dashboard", info_message)
            return Response({"success": False, "error": str(info_message)})


class GendocxView(APIView):
    """ download word template"""
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        get_language = set_session_language(request)
        try:
            print(request.user)
            word_serializer = WordTemplateSerializer(data=request.data)
            if word_serializer.is_valid():
                word_serializer.save()
            template = 'media/word_template/ganesh.docx'
            user = {
                'name': request.user.username,
                'email': request.user.email
            }
            document = generate.from_template(template, user)
            document.seek(0)
            bytesio_object = document
            with open("media/copy.docx", 'wb') as f:
                f.write(bytesio_object.getbuffer())
            url = "/media/copy.docx"
            return Response({"url": url})
        except Exception as e:
            info_message = get_info_messages(get_language, 'download_profile_error')
            print("Unable to download Profile", info_message)
            print("exception in downloading profile", e)
            return Response({"success": False, "error": str(info_message)})



class GetLabels(APIView):
    """Gets labels from the database."""
    def post(self, request):
        get_language = set_session_language(request)
        try:
            jsondata = request.data
            print(jsondata)
            page_name = jsondata['page_name']
            language_id = jsondata['language_id']
            if jsondata['language_id'] == None:
                language_id = 1
            get_language_name = Language.objects.filter(id=language_id).values('id')
   
            language_name_id = get_language_name[0]['id']
            
            if request.session['language'] == language_name_id:
                pass
            else:
                request.session['language'] = language_name_id
            print('language_name_id', language_name_id )

            get_page_name_id = PageName.objects.filter(
                            language_name_id=language_name_id).filter(page_name=page_name).values('id')

            page_name_id = get_page_name_id[0]['id']
            print(page_name_id)

            page_labels = list(PageLabel.objects.filter(
                               page_name_id=page_name_id).values('page_label_class_name', 'page_label_text'))
            print(page_labels)
            return JsonResponse(page_labels, safe=False)
        except Exception as e:
            info_message = get_info_messages(get_language, 'label_error')
            print("Cannot fetch labels from database", info_message)
            print("exception in getting label", e)
            return JsonResponse({"success": False, "error": str(info_message)}, status=404)


class GetLangauges(APIView):
    """Gets labels from the database."""
    def get(self, request):
        get_language = set_session_language(request)
        try:
            get_languages = Language.objects.all().values('id','language_name')
            print('lan', get_languages[0])
            request.session['language'] = get_languages[0]['id']

            print("set language ", request.session['language'] )
            language_list = []
            for language in get_languages:
                language_list.append(language)
            print(language_list)
            return JsonResponse(language_list, safe=False)
        except Exception as e:
            info_message = get_info_messages(get_language, 'language_error')
            print("Cannot fetch languages from database", info_message)
            print("exception in getting label", e)
            return JsonResponse({"success": False, "error": str(info_message)}, status=404)

class GetToast(APIView):
    def post(self, request):
        get_language = set_session_language(request)
        try:
            jsondata = request.data
            print(jsondata)
            info_message = get_info_messages(get_language, jsondata['toast_label'])
            message = {"message": info_message}
            return JsonResponse(message, safe=False)

        except Exception as e:
            print("exception in toast message", e)
            info_message = get_info_messages(get_language, 'internal_server_error')
            print(info_message)
            return JsonResponse({'error' : str(info_message)}, status=500)
