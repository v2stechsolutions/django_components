from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import json
from .models import UserRegisterationModel, UserQualification, UserRole
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.views import APIView
from django.utils.dateparse import parse_date 
from .user_registration_form import UserRegisterationForm, UserForm
from django.db import transaction
from user_authentication.views import set_session_language
from user_authentication.get_info_msg import get_info_messages, set_session_language

# Create your views here.

class RegistrationFormView(APIView):
    """Registration Form."""

    def get(self, request):
        """Renders Registration form."""  
                                              
        get_language = set_session_language(request)

        try:
            return render(request, 'user_registration/registration_form.html')

        except Exception as e:
            print("Error in getting registeration page:", e)
            info_message = get_info_messages(get_language, "registration_exception")
            print("Cannot get the registeration page.", info_message)
            return  JsonResponse({"error": str(info_message)}, status=500)
    
    def post(self, request):
        """Submits and saves user data into the database."""

        get_language = set_session_language(request)

        try:
            user_data = request.POST
            user_file = request.FILES
            print('#'*80)
            print(user_data)
            print('#'*80)
            print(user_file)
            print('#'*80)
            if User.objects.filter(username=user_data['user_name']).exists():
                info_message = get_info_messages(get_language, "username_exception")
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
            check_register_data['role']=3
           
          
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
                        info_message = get_info_messages(get_language, "register_success_message")
                        print("Welcome {}, you have successfully registered.", info_message)
                        success_msg = info_message.format(check_register_data['first_name'])
                        return JsonResponse({'message' : success_msg})
                    else:
                        print(details.errors)
                        print(one_user.errors)
                        info_message = get_info_messages(get_language, "register_data_invalid")
                        print("Invalid data", info_message)
                        return JsonResponse({'error' : str(info_message)}, status=500)
            except Exception as e:
                info_message = get_info_messages(get_language, "rollback_error")
                print("Please try again saving the data", info_message)
                print("exception in saving data rollback error", e)
                return JsonResponse({'error' : str(info_message)}, status=500)

        
        except Exception as e:
            print("Error in submitting form:", e)
            info_message = get_info_messages(get_language, "internal_server_error")
            print("sometime went wrong", info_message)
            return JsonResponse({'error': str(info_message) }, status=500)



class CheckUsername(APIView):
    """Checks whether username is available."""

    def post(self, request):

        get_language = set_session_language(request)
        try:
            if request.method == 'POST':
                jsondata = request.POST
                print(jsondata['user_name'])
                try:
                    if User.objects.filter(username=jsondata['user_name']).exists():
                        info_message = get_info_messages(get_language, 'username_exception')
                        print("Username already taken!", info_message)
                        return JsonResponse({'message': 'taken', 'toast_msg':str(info_message)})
                except Exception as e:
                    print("username except", e)
                else:
                    info_message = get_info_messages(get_language, "username_success")
                    print("Username Available...!!!", info_message)
                    return JsonResponse({'message': 'not_taken', 'toast_msg':str(info_message)})
        except Exception as e:
            print("exception in check username", e)
            info_message = get_info_messages(get_language, 'internal_server_error')
            print(info_message)
            return JsonResponse({'error' : str(info_message)}, status=500)

class CheckEmail(APIView):
    """Checks whether email id is already registered or not."""

    def post(self, request):

        get_language = set_session_language(request)
        try:
            if request.method == 'POST':
                jsondata = request.POST

                if User.objects.filter(email=jsondata['email']).exists():
                    info_message = get_info_messages(get_language, "email_exception")
                    print("Email Id  already registered!", info_message)
                    return JsonResponse({'message': 'taken', 'toast_msg': str(info_message)})
                else:
                    info_message = get_info_messages(get_language, 'email_success')
                    print("Email Id not registered", info_message)
                    return JsonResponse({'message': 'not_taken', 'toast_msg': str(info_message)})
        except Exception as e:
            info_message = get_info_messages(get_language, 'internal_server_error')
            print(info_message)
            print("exception in check username", e)
            return JsonResponse({'error' : str(info_message)}, status=500)

class GetQualificationDropDown(APIView):
    """Gets qualification dropdown from the database."""
    def get(self, request):

        get_language = set_session_language(request)

        try:
            get_qualification = UserQualification.objects.all().values('qualification_no','qualification_name')
            print('qualification', get_qualification[0])
            qualification_list = []
            for qualification in get_qualification:
                qualification_list.append(qualification)
            print(qualification)
            return JsonResponse(qualification_list, safe=False)
        except Exception as e:
            info_message = get_info_messages(get_language, 'qualification_dropdown_fail')
            print("Cannot fetch  qualification dropdown from database", info_message)
            print("exception in getting label", e)
            return JsonResponse({"success": False, "error": str(info_message)}, status=404)

class GetRoleDropDown(APIView):
    """Gets qualification dropdown from the database."""
    def get(self, request):
        get_language = set_session_language(request)

        try:
            get_role= UserRole.objects.all().values('role_no','role_name')
            print('qualification', get_role[0])
            role_list = []
            for role in get_role:
                role_list.append(role)
            print(role_list)
            
            return JsonResponse(role_list, safe=False)
        except Exception as e:
            print("exception in getting label", e)
            info_message = get_info_messages(get_language, 'role_dropdown_fail')
            print("Cannot fetch Role dropdown from database", info_message)
            return JsonResponse({"success": False, "error": str(info_message)}, status=404)