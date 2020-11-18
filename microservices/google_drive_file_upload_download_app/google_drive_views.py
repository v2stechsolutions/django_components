import os
import glob
from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from django.http.response import JsonResponse
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth
from .google_drive_serializers import FileSerializer

class GoogleDriveHomeView(APIView):
    def get(self, request):
        return render(request, 'google_drive/home.html')

    def post(self, request):
        file_serializer = FileSerializer(data=request.data)
        print('G'*80)
        print(file_serializer)
        print('F'*80)
        if file_serializer.is_valid():
            print('R'*80)
            file_serializer.save()
            print('Q'*80)

            uploaded_data = request.data
            latest_file_name = uploaded_data['file']

            path = settings.BASE_DIR + '/media/DriveUpload/'

            try:
                #google drive api authentication
                gauth = GoogleAuth()
                gauth.LoadCredentialsFile("mycreds.txt")

                if gauth.credentials is None:
                    gauth.LocalWebserverAuth()
                elif gauth.access_token_expired:
                    gauth.Refresh()
                else:
                    gauth.Authorize()

                gauth.SaveCredentialsFile("mycreds.txt")
                drive = GoogleDrive(gauth)

                #upload file in google drive using path and file name
                f = drive.CreateFile({"title" : str(latest_file_name)})
                f.SetContentFile(os.path.join(path, str(latest_file_name)))
                f.Upload()
                os.remove(path+str(latest_file_name))
                return Response({'message' : 'File uploaded successsfully.'})
            
            except Exception as e:
                print(e)
                uploaded_files = glob.glob(path + '*')

                for f in uploaded_files:
                    os.remove(f)
                return Response({'message' : 'Please check internet connection.'})

        else:
            return Response(file_serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

class GoogleDriveFileListView(APIView):
    def get(self, request):
        all_files = []
        all_files_obj = {}
        try:
            gauth = GoogleAuth()
            gauth.LoadCredentialsFile("mycreds.txt")

            if gauth.credentials is None:
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                gauth.Refresh()
            else:
                gauth.Authorize()

            gauth.SaveCredentialsFile("mycreds.txt")
            drive = GoogleDrive(gauth)

            parent = 'root'
            file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
            for each in file_list:
                if '.' in  each['title']:
                    all_files_obj['id'] = each['id']
                    all_files_obj['title'] = each['title']
                    all_files.append(all_files_obj.copy())        
            return JsonResponse({"FileList" : all_files})
        except:
            return JsonResponse({"Message" : "Please check internet connection."})

class GoogleDriveFileUploadView(APIView):
    def post(self, request):
        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()

            uploaded_data = request.data
            latest_file_name = uploaded_data['file']

            path = settings.BASE_DIR + '/media/DriveUpload/'

            try:
                #google drive api authentication
                gauth = GoogleAuth()
                gauth.LoadCredentialsFile("mycreds.txt")

                if gauth.credentials is None:
                    gauth.LocalWebserverAuth()
                elif gauth.access_token_expired:
                    gauth.Refresh()
                else:
                    gauth.Authorize()

                gauth.SaveCredentialsFile("mycreds.txt")
                drive = GoogleDrive(gauth)

                #upload file in google drive using path and file name
                f = drive.CreateFile({"title" : str(latest_file_name)})
                f.SetContentFile(os.path.join(path, str(latest_file_name)))
                f.Upload()
                os.remove(path+str(latest_file_name))
                return Response({'message' : 'File uploaded successsfully.'})
            
            except:
                uploaded_files = glob.glob(path + '*')

                for f in uploaded_files:
                    os.remove(f)
                return Response({'message' : 'Please check internet connection.'})

        else:
            return Response(file_serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

class GoogleDriveFileDownloadView(APIView):
    def post(self, request):
        data = request.data

        try:
            #google drive api authentication
            gauth = GoogleAuth()
            gauth.LoadCredentialsFile("mycreds.txt")
            if gauth.credentials is None:
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                gauth.Refresh()
            else:
                gauth.Authorize()

            gauth.SaveCredentialsFile("mycreds.txt")
            drive = GoogleDrive(gauth)

            url_id = data['id']

            file_obj = drive.CreateFile({'id': url_id})
            
            #download file from google drive using file id
            try:
                folder = settings.BASE_DIR + '/media/DriveDownload'

                if not os.path.exists(folder):
                    os.makedirs(folder)
                destination_uri = '{}/{}'.format(folder, file_obj['title'])

                file_obj.GetContentFile(destination_uri)
                return Response({'message' : 'File Downloaded Successsfully.'})
            except:
                return Response({'message' : 'File Downloading Failed.Please check url.'})
        except:
            return Response({'message' : 'Please check internet connection.'})