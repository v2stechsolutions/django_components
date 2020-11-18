import os
import glob
import datetime
from django.http import Http404
from django.conf import settings
from django.http.response import JsonResponse
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth
from google.cloud import storage
from .google_cloud_bucket_serializers import FileSerializer
from .google_cloud_bucket_models import File


#get all files list from google cloud bucket
class CloudBucketFileListView(APIView):
    def get(self, request):
        allFilesInCloud = []
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'creds.json'
            storage_client = storage.Client()
            blobs = storage_client.list_blobs('demo_upload_bucket')

            for blob in blobs:
                allFilesInCloud.append(blob.name)
            return JsonResponse({"FileList" : allFilesInCloud})
        except:
            return JsonResponse({"Message" : "Please check internet connection."})

class CloudBucketFileUpload(APIView):
    def post(self, request):
        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            # file_serializer.save()

            uploaded_data = request.data
            latest_file_name = uploaded_data['file']
            
            path = settings.BASE_DIR + '/static/cloudUpload/'
            
            try:
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'creds.json'
                storage_client = storage.Client()
                bucket = storage_client.bucket("demo_upload_bucket")

                blob = bucket.blob(str(latest_file_name))

                #Upload file in bucket
                # blob.upload_from_filename(path + str(latest_file_name))
                os.remove(path + str(latest_file_name))

                signed_url = blob.generate_signed_url(version='v4',expiration=datetime.timedelta(minutes=30),method='POST', )

                return Response({'signed_url' : signed_url})
            except:
                uploaded_files = glob.glob(path + '*')
                for f in uploaded_files:
                    os.remove(f)
                return Response({"message" : "Please check internet connection."})
        else:
            return Response(file_serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)

class CloudBucketFileDownload(APIView):
    def post(self, request):
        data = request.data
        destination_file_name = data['filename']

        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'creds.json'
            storage_client = storage.Client()

            bucket_name = "demo_upload_bucket"
            bucket = storage_client.bucket(bucket_name)

            #download file from bucket
            blob = bucket.blob(destination_file_name)
            folder = settings.BASE_DIR + '/static/cloudDownload'

            if not os.path.exists(folder):
                os.makedirs(folder)
                
            destination_uri = '{}/{}'.format(folder, destination_file_name)
            blob.download_to_filename(destination_uri)
            return Response({'message' : 'File downloaded successfully.'})
        except:
            return Response({'message' : 'Please check internet connection.'})