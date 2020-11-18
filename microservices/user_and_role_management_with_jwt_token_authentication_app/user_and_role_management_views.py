import requests
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .user_and_role_management_models import User, Role, Permission
from .user_and_role_management_serializers import UserSerializer, RoleSerializer, PermissionSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User as DefaultUser, Group, Permission as DefaultPermission
from django.core import serializers
from django.forms.models import model_to_dict
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator 
from django.contrib.auth.decorators import login_required



def userPermission(username, permissionName):
    if username == 'superuser':
        return True
    else:
        user = User.objects.filter(username=username).values('role_id')
        user_list = list(user)
        role_id = user_list[0]['role_id']
        permission = Permission.objects.filter(role_id=role_id).values('add_user','edit_user','delete_user','add_role','edit_role','delete_role')
        permission_list = list(permission)
        check_permission = permission_list[0][permissionName]
        return check_permission

class PermissionIdView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk):
        edit_permission = Permission.objects.filter(role_id=pk).values('add_user','edit_user','delete_user','add_role','edit_role','delete_role')
        edit_permission_list = list(edit_permission)
        return JsonResponse({'message' : edit_permission_list[0]})

    def put(self, request, pk):
        try:
            permission = Permission.objects.get(pk=pk)
        except permission.DoesNotExist:
            return JsonResponse({'message': 'The permission does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)

        permission_data = JSONParser().parse(request)
        permission_serializer_edit = PermissionSerializer(permission, data=permission_data)

        if permission_serializer_edit.is_valid():
            username = request.user.username
            has_permission = userPermission(username, 'edit_role')
            if has_permission == False:
                return JsonResponse({'message' : 'You have no permission'})
            else:
                permission_serializer_edit.save()
                return JsonResponse(permission_serializer_edit.data)
        return JsonResponse(permission_serializer_edit.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

class DjangoLogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        logout(request)
        return JsonResponse({'message' : 'Logged out successfully'})

class UserwebpageHtmlView(APIView):
    def get(self, request):
        return render(request, 'user_management/userwebpage.html')

class UserwebpageView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return render(request, 'user_management/userwebpage.html')

class RolewebpageHtmlView(APIView):
    def get(self, request):
        return render(request, 'user_management/rolewebpage.html')

class RolewebpageView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return render(request, 'user_management/rolewebpage.html')

class DashboardHtmlView(APIView):

    def get(self, request):
        return render(request, 'user_management/dashboard.html')

class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return render(request, 'user_management/dashboard.html')

class LoginView(APIView):
    def get(self, request):
        return render(request, 'user_management/login.html')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            refresh = self.get_token(self.user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            return data
        except:
            status = {'status' : 'Please enter valid credentials'}
            return status

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class DjangoLoginView(APIView):
    def checkPermissions(self,username):

        user = User.objects.filter(username=username).values('role_id')
        user_list = list(user)
        role_id = user_list[0]['role_id']
        permission = Permission.objects.filter(role_id=role_id).values('add_user','edit_user','delete_user','add_role','edit_role','delete_role')
        permission_list = list(permission)
        p_obj = {}
        p_list = []
        for each in permission_list:
            p_obj['add_user'] = each['add_user']
            p_obj['edit_user'] = each['edit_user']
            p_obj['delete_user'] = each['delete_user']
            p_obj['add_role'] = each['add_role']
            p_obj['edit_role'] = each['edit_role']
            p_obj['delete_role'] = each['delete_role']
            p_list.append(p_obj)
        return p_list

    def post(self, request):

        login_data = JSONParser().parse(request)
        username = login_data['username']
        password = login_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            username = request.user.username
            is_superuser = request.user.is_superuser

            if(is_superuser == True):
                permission_list = [{'add_user': True, 'edit_user':True,
                                    'delete_user': True, 'add_role': True,
                                    'edit_role':True, 'delete_role': True}]
            else:
                permission_list = self.checkPermissions(username)
            
            return JsonResponse({'message' : permission_list})
        else:
            return JsonResponse({'message' : 'Please enter valid credentials'})
            
class PermissionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        permission = Permission.objects.all()

        permission_list = []
        for each in permission:
            permission_list.append(str(each))
        return JsonResponse(permission_list, safe= False)

    def post(self, request):
        Permission_data = JSONParser().parse(request)

        permission_serializer = PermissionSerializer(data=Permission_data)

        if permission_serializer.is_valid():
            permission_serializer.save()
            return JsonResponse(permission_serializer.data,
                                status = status.HTTP_201_CREATED)
        return JsonResponse(permission_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class RoleView(APIView):
    permission_classes = (IsAuthenticated,)
    
    #get role list from database
    def get(self, request):

        if request.user.is_authenticated:

            roles = Role.objects.all()
            roles_serializer = RoleSerializer(roles, many=True)
            return JsonResponse(roles_serializer.data, safe=False)

    #add roles in database
    def post(self, request):
        
        roles_data = JSONParser().parse(request)
        roles_serializer = RoleSerializer(data=roles_data)

        if roles_serializer.is_valid():
            if request.user.is_authenticated:
                username = request.user.username
                has_permission = userPermission(username, 'add_role')
                if has_permission == False:
                    return JsonResponse({'message' : 'You have no permission'})
                else:
                    roles_serializer.save()
                    return JsonResponse(roles_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(roles_serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)


class RoleIdBasedView(APIView):
    permission_classes = (IsAuthenticated,)

    #get role from database using role id
    def get(self, request, pk):

        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return JsonResponse({'message': 'The Role does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)

        roles_serializer = RoleSerializer(role)
        return JsonResponse(roles_serializer.data)

    #update role in database using role id
    def put(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return JsonResponse({'message': 'The Role does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)

        roles_data = JSONParser().parse(request)
        roles_serializer = RoleSerializer(role, data=roles_data)

        if roles_serializer.is_valid():
            roles_serializer.save()
            return JsonResponse(roles_serializer.data)
            
        return JsonResponse(roles_serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

    #delete role from database using role id
    def delete(self, request, pk):
        try:
            role = Role.objects.get(pk=pk)
            username = request.user.username
            has_permission = userPermission(username, 'delete_role')

            if has_permission == False:
                return JsonResponse({'message' : 'You have no permission'})
            else:
                role.delete()
        except Role.DoesNotExist:
            return JsonResponse({'message': 'The Role does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({'message': 'Role was deleted successfully!'}, 
                            status=status.HTTP_204_NO_CONTENT)


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    #get userlist from database
    def get(self, request):
        users = User.objects.all()

        username = request.GET.get('username', None)
        if username is not None:
            users = users.filter(username__icontains=username)
                
        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)

     #add user in database
    def post(self, request):
        user_data = JSONParser().parse(request)
        users_serializer = UserSerializer(data=user_data)

        if users_serializer.is_valid():
            users_serializer.save()
            first_name = user_data['first_name']
            last_name = user_data['last_name']
            username = user_data['username']
            password = user_data['password']
            email = user_data['email']
            default_user = DefaultUser.objects.create_user(username = username, password = password, email = email, first_name = first_name, last_name = last_name)
            username = request.user.username
            has_permission = userPermission(username, 'add_user')
            if has_permission == False:
                return JsonResponse({'message' : 'You have no permission'})
            else:
                default_user.save()
            return JsonResponse(users_serializer.data, 
                                status=status.HTTP_201_CREATED) 
        return JsonResponse(users_serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)


class UserIdBasedView(APIView):
    permission_classes = (IsAuthenticated,)

    #get user from database using user id
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'message': 'The User does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)

        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data)
    
    #update user in database using user id
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'message': 'The User does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)

        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(user, data=user_data)

        if user_serializer.is_valid():
            username = request.user.username
            has_permission = userPermission(username, 'edit_user')
            if has_permission == False:
                return JsonResponse({'message' : 'You have no permission'})
            else:
                user_serializer.save()
                return JsonResponse(user_serializer.data)
        return JsonResponse(user_serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

    #delete user from database using user id
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            username = request.user.username
            has_permission = userPermission(username, 'delete_user')
            if has_permission == False:
                return JsonResponse({'message' : 'You have no permission'})
            else:
                user.delete()

        except User.DoesNotExist:
            return JsonResponse({'message': 'The User does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({'message': 'User was deleted successfully!'}, 
                            status=status.HTTP_204_NO_CONTENT)