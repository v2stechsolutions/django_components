from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .user_and_role_management_models import User, Role
from .user_and_role_management_serializers import UserSerializer, RoleSerializer

class RoleView(APIView):
    permission_classes = (IsAuthenticated,)

    #get role list from database
    def get(self, request):
        roles = Role.objects.all()
        roles_serializer = RoleSerializer(roles, many=True)
        return JsonResponse(roles_serializer.data, safe=False)

    #add roles in database
    def post(self, request):
        roles_data = JSONParser().parse(request)
        roles_serializer = RoleSerializer(data=roles_data)

        if roles_serializer.is_valid():
            roles_serializer.save()
            return JsonResponse(roles_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(roles_serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

    #delete all roles in database
    def delete(self, request):
        count = Role.objects.all().delete()
        return JsonResponse({'message' : '{} roles were deleted successfully!'.format(count[0])}, 
                            status=status.HTTP_204_NO_CONTENT)

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
        except Role.DoesNotExist:
            return JsonResponse({'message': 'The Role does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)

        role.delete()
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
            return JsonResponse(users_serializer.data, 
                                status=status.HTTP_201_CREATED) 
        return JsonResponse(users_serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

    #delete all users from database
    def delete(self, request):
        count = User.objects.all().delete()
        return JsonResponse({'message': '{} Users were deleted successfully!'.format(count[0])}, 
                            status=status.HTTP_204_NO_CONTENT)

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
            user_serializer.save()
            return JsonResponse(user_serializer.data)
        return JsonResponse(user_serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

    #delete user from database using user id
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return JsonResponse({'message': 'The User does not exist'}, 
                                status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return JsonResponse({'message': 'User was deleted successfully!'}, 
                            status=status.HTTP_204_NO_CONTENT)