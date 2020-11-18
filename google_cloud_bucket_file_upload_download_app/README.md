# FILE UPLOAD AND DOWNLOAD FROM GOOGLE CLOUD STORAGE

This app helps you to upload and download file from google cloud storage

Copy and paste this app in your project

Add this app under INSTALLED_APPS section in settings.py

## Usage 

```bash
/filelist
```

no parameters required

Get list of all files available in google cloud bucket

```bash
/upload
```

Parameters required : 

file : select file to upload on cloud

Uploads selected file in google cloud bucket

```bash
/download
```

Parameters required : 

filename : Filename which suppose to be download from google cloud bucket

Downloads selected file from google cloud bucket

