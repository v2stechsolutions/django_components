from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from . import generate
from django.core.files.storage import FileSystemStorage
import json
from .serializer import WordTemplateSerializer
import docx
import os

# Create your views here.
class GendocxView(APIView):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        word_serializer = WordTemplateSerializer(data=request.data)
    
        if word_serializer.is_valid():
            word_serializer.save()

        template = 'media/word_template/{}'.format(request.data['word_template'])
        # signature = 'signature.png'
        signature = 'media/signature/{}'.format(request.data['signature'])
        a = open('media/json/{}'.format(request.data['json']))
        docx_json_string = a.read()
        docx_json = json.loads(docx_json_string)

        document = generate.from_template(template, signature, docx_json)
        document.seek(0)

        # bytesio_object = document
        # with open("copy.docx",'wb') as f:
        #     f.write(bytesio_object.getbuffer())

        response = HttpResponse(document, content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename= invoice.docx'

        return response
