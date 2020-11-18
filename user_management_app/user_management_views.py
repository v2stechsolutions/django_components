from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from django.contrib.auth.models import User
from user_registeration.models import UserRegisterationModel, LevelModel
from .user_management_serializer import UserRegisterationModelSerializer, UserRegisterationModelFileSerializer, AuthUserSerializer, DatatableSerializer
from user_registeration.models import UserRegisterationModel
from user_registeration.user_registration_form import UserRegisterationForm, UserForm
from user_registeration.models import query_users_by_args
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from user_authentication.get_info_msg import set_session_language, get_info_messages
from user_authentication.views import CustomJWTAuthentication
# Create your views here.


class GetAllUsersView(APIView):
    """Return filtered Users details from database to display in datatable """
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self, request):

        get_language = set_session_language(request)

        try:
            datatable_server_processing = query_users_by_args(request, **request.query_params)
            serializer = DatatableSerializer(datatable_server_processing['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = datatable_server_processing['draw']
            result['recordsTotal'] = datatable_server_processing['total']
            result['recordsFiltered'] = datatable_server_processing['count']
            return Response(result)
        except Exception as e:
            print("Exception in getting  all user", e)
            info_message = get_info_messages(get_language, 'get_user_error')
            print("Cannot fetch all users data from database", info_message)
            return JsonResponse({'message' : str(info_message)}, status = 422)

class EditUserFormView(APIView):
    """Get, Delete and Update user using User Id """
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk):
        """Get User details using User Id"""

        get_language = set_session_language(request)

        try:
            check_user_is_superuser = User.objects.filter(id = request.user.id).values('is_superuser')
            if check_user_is_superuser[0]['is_superuser'] == True:
                pass
            else:
                role_of_user = UserRegisterationModel.objects.filter(user_id = request.user.id).values('role')
                has_permission = LevelModel.objects.filter(level_id = role_of_user[0]['role']).values('view_user')
                if(has_permission[0]['view_user'] == True):
                    pass
                else:
                    info_message = get_info_messages(get_language, 'view_permission')
                    print("no permission to view user", info_message)
                    return JsonResponse({'message' : info_message})

            is_user_found = User.objects.filter(id = pk).exists()
            if is_user_found == False:
                info_message = get_info_messages(get_language, 'user_not_found')
                print("User Not found", info_message)
                return JsonResponse({'message' : info_message},status = 404)
            user = User.objects.get(id = pk)
            register = UserRegisterationModel.objects.filter(user_name = user.username).values\
                                                            ('user_name','first_name','middle_name',
                                                            'last_name', 'dob', 'email', 'telephone',
                                                            'gender', 'address', 'indian', 'option',
                                                            'profile_picture','resume',
                                                            'pan_card','adhar_card','role')
            info_message = get_info_messages(get_language, 'get_user_error')
            print("Cannot fetch all users data from database", info_message)
            return JsonResponse({'message' : list(register)})
        except Exception as e :
            print("Exception in getting  all user", e)
            info_message = get_info_messages(get_language, 'user_data_error')
            print("Cannot get the data of the user", info_message)
            return JsonResponse({'message' : str(info_message)}, status =422)

    def delete(self, request, pk):
        """Delete user using User Id"""

        get_language = set_session_language(request)

        try:
            check_user_is_superuser = User.objects.filter(id = request.user.id).values('is_superuser')
            if check_user_is_superuser[0]['is_superuser'] == True:
                pass
            else:
                role_of_user = UserRegisterationModel.objects.filter(user_id = request.user.id).values('role')
                has_permission = LevelModel.objects.filter(level_id = role_of_user[0]['role']).values('delete_user')
                if(has_permission[0]['delete_user'] == True):
                    pass
                else:
                    info_message = get_info_messages(get_language, 'delete_permission')
                    print("no permission to delete user", info_message)
                    return JsonResponse({'message' : info_message})
            is_user_found = User.objects.filter(id = pk).exists()
            if is_user_found == False:
                info_message = get_info_messages(get_language, 'user_not_found')
                print("User Not found", info_message)
                return JsonResponse({'message' : info_message},status = 404)
            user = User.objects.get(id = pk)
            register = UserRegisterationModel.objects.get(user_name = user.username)
            try:
                with transaction.atomic():
                    user.delete()
                    register.delete()
                    info_message = get_info_messages(get_language, 'delete_success')
                    print("User {} deleted successfully".format(user.username))
                    success_msg = "User {} deleted successfully".format(user.username)
                    return JsonResponse({'message' : success_msg})
            except Exception as e:
                info_message = get_info_messages(get_language, 'rollback_error')
                print("Please try again", info_message)
                print("exception in saving data rollback error", e)
                return JsonResponse({'error' : str(info_message)}, status=422)
            
        except Exception as error:
            print("delete", error)
            info_message = get_info_messages(get_language, 'internal_server_error')
            print("Internal Server Error", info_message)
            return JsonResponse({'message' : str(info_message)},status = 422)

    def put(self, request, pk):
        """Update user details using User Id"""

        get_language = set_session_language(request)

        try:
            check_user_is_superuser = User.objects.filter(id = request.user.id).values('is_superuser')
            if check_user_is_superuser[0]['is_superuser'] == True:
                pass
            else:
                role_of_user = UserRegisterationModel.objects.filter(user_id = request.user.id).values('role')
                has_permission = LevelModel.objects.filter(level_id = role_of_user[0]['role']).values('edit_user')
                if(has_permission[0]['edit_user'] == True):
                    pass
                else:
                    info_message = get_info_messages(get_language, 'edit_permission')
                    print("no permission to edit user", info_message)
                    return JsonResponse({'message' : info_message})
            is_user_found = User.objects.filter(id = pk).exists()
            if is_user_found == False:
                info_message = get_info_messages(get_language, 'user_not_found')
                print("User Not found", info_message)
                return JsonResponse({'message' : info_message},status = 404)

            user = User.objects.get(pk = pk)        
            edited_user = UserRegisterationModel.objects.get(user_name = user.username)


            edit_serializer = UserRegisterationModelSerializer(edited_user, data=request.POST)
            edit_file_serialier = UserRegisterationModelFileSerializer(edited_user, data = request.FILES)
            auth_user_serializer = AuthUserSerializer(user, data = {"username" : request.POST['user_name'],
                                                                    "email" : request.POST['email'],
                                                                    "password" : request.POST['password']})
            try:
                with transaction.atomic():
                    if(edit_serializer.is_valid()):
                        if(edit_file_serialier.is_valid()):
                            if(auth_user_serializer.is_valid()):
                                edit_serializer.save()                                                                                                                                                    
                                edit_file_serialier.save()
                                auth_user_instance = auth_user_serializer.save()
                                auth_user_instance.set_password(auth_user_instance.password)
                                auth_user_instance.save()
                                info_message = get_info_messages(get_language, 'update_user')
                                print('User {} updated successfully'.format(request.POST['user_name']))
                                success_msg = 'User {} updated successfully'\
                                                    .format(request.POST['user_name'])
                                return JsonResponse({'message' : success_msg})
                            else:
                                info_message = get_info_messages(get_language, 'internal_server_error')
                                print("serializer error", auth_user_serializer.errors)
                                print("Internal Server Error", info_message)
                                return JsonResponse({'message' : str(info_message)}, status = 422)
                        else:
                            info_message = get_info_messages(get_language, 'internal_server_error')
                            print("serializer error", edit_file_serialier.errors)
                            print("Internal Server Error", info_message)
                            return JsonResponse({'message' : str(info_message)}, status = 422)
                    else:
                        info_message = get_info_messages(get_language, 'internal_server_error')
                        print("serializer error", edit_serializer.errors)
                        print("Internal Server Error", info_message)
                        return JsonResponse({'message' : str(info_message)}, status = 422)
            except Exception as e:
                print("exception in saving data rollback error", e)
                info_message = get_info_messages(get_language, 'rollback_error')
                print("Please try again saving the data", info_message)
                return JsonResponse({'message' : str(info_message)}, status=422)  
        except Exception as error:
            info_message = get_info_messages(get_language, 'internal_server_error')
            print("Internal Server Error", info_message, error)
            return JsonResponse({'message' : str(info_message)},status = 422)

class AddUserPageFormView(APIView):
    def get(self, request):
        """Renders Add user form."""

        get_language = set_session_language(request)

        try:
            return render(request, 'user_management/add_user.html')

        except Exception as e:
            print("Error in getting registeration page:", e)
            info_message = get_info_messages(get_language, 'registration_exception')
            print("Cannot get the registeration page.", info_message)
            return  JsonResponse({"error": str(info_message)}, status=404)

class AddUserFormView(APIView):
    """Add new user form."""
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """Submits and saves user data into the database."""

        get_language = set_session_language(request)

        try:
            check_user_is_superuser = User.objects.filter(id = request.user.id).values('is_superuser')
            if check_user_is_superuser[0]['is_superuser'] == True:
                pass
            else:
                role_of_user = UserRegisterationModel.objects.filter(user_id = request.user.id).values('role')
                has_permission = LevelModel.objects.filter(level_id = role_of_user[0]['role']).values('add_user')
                if(has_permission[0]['add_user'] == True):
                    pass
                else:
                    info_message = get_info_messages(get_language, 'add_permission')
                    print("no permission to add user", info_message)
                    return JsonResponse({'message' : info_message})
            user_data = request.POST
            user_file = request.FILES
            print('#'*80)
            print(user_data)
            print('#'*80)
            print(user_file)
            print('#'*80)

            if User.objects.filter(username=user_data['user_name']).exists():
                info_message = get_info_messages(get_language, 'username_exception')
                print("Username already taken!", info_message)
                return JsonResponse({'message' : info_message})
            
            auth_data = {
                "username" : user_data['user_name'],
                "email" : user_data['email'],
                "password" : user_data['password']
            }

            print('A'*80)
            print(auth_data)
            print('A'*80)
           
            check_register_data = user_data
            _mutable = check_register_data._mutable

            # set to mutable
            check_register_data._mutable = True

            # сhange the values you want
            check_register_data.pop('password', None)
            # check_register_data['role']="Customer"
           
            check_register_data._mutable = _mutable
            print(check_register_data)
            details = UserRegisterationForm(check_register_data, request.FILES)
            one_user = UserForm(data=auth_data)
            print(details.is_valid)
            print(one_user.is_valid)

            try:
                with transaction.atomic():
                    if details.is_valid() and one_user.is_valid(): 
                        user = one_user.save(commit=False)
                        user.set_password(auth_data['password'])
                        user.save()
                        user_data = details.save(commit=False)
                        user_data.user = user
                        user_data.save()
                        print("user", user)
                        print("user_data", user_data)
                        print("form is validated")
                        info_message = get_info_messages(get_language, 'user_add_success')
                        print("User {}, have successfully created.".format(check_register_data['first_name']))
                        success_msg = "User {}, have successfully created.".format(check_register_data['first_name'])
                        return JsonResponse({'message' : success_msg})
                    else:
                        print(details.errors)
                        print(one_user.errors)
                        info_message = get_info_messages(get_language, 'register_data_invalid')
                        print("Invalid data", info_message)
                        return JsonResponse({'error' : str(info_message)}, status=500)
            except Exception as e:
                info_message = get_info_messages(get_language, 'rollback_error')
                print('Please try again saving the data', info_message)
                print("exception in saving data rollback error", e)
                return JsonResponse({'error' : str(info_message)}, status=500)
         
        
        except Exception as e:
            print("Error in submitting form:", e)
            info_message = get_info_messages(get_language, 'internal_server_error')
            print("Internal Server Error", info_message)
            return JsonResponse({'error': str(info_message) }, status=500)


class GetPermissions(APIView):
    """Get Permissons of user"""

    def post(self, request):
        get_language = set_session_language(request)
        
        try:
            jsondata = JSONParser().parse(request)
            check_user_is_superuser = User.objects.filter(id = jsondata['user_id']).values('is_superuser')
            print("1"*20, check_user_is_superuser)
            if check_user_is_superuser[0]['is_superuser'] == True:
                perms = LevelModel.objects.filter(level_id = 1)\
                        .values('add_user', 'view_user', 'edit_user', 'delete_user')
                perms_dict = perms[0]
                perms_dict["level"] = True
                print("2"*20,perms_dict)
                return JsonResponse(perms_dict)
            if(jsondata['user_role_id'] == 1):
                user_level = True
                print("3"*20, user_level)
            else:
                user_level = False
                print("4"*20, user_level)
            perms = LevelModel.objects.filter(level_id = jsondata['user_role_id'])\
                    .values('add_user', 'view_user', 'edit_user', 'delete_user')
            perms_dict = perms[0]
            print("5"*20, perms_dict)
            perms_dict["level"] = user_level
            print("6"*20, perms_dict['level'])
            return JsonResponse(perms_dict)
        except Exception as error:
            info_message = get_info_messages(get_language, 'get_permission_error')
            print("Permission fetching  issue due to Internal Server Error", info_message, error)
            return JsonResponse({'message' : str(info_message)},status = 422)