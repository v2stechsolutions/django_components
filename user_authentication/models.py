from django.db import models

# Create your models here.

class WordTemplate(models.Model):
    word_template = models.FileField(upload_to = 'word_template', blank=False)
    json = models.FileField(upload_to = 'json', blank=False)
    signature = models.FileField(upload_to = 'signature', blank = False)