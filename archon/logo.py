from django.shortcuts import render
#from django.conf import settings
from django.core.files.storage import FileSystemStorage
from . import settings
import os


def upload(request):
    if request.method == 'POST' and request.FILES['logo']:
        myfile = request.FILES['logo']
        fs = FileSystemStorage( "/tmp")
        filename = fs.save( "logo.png", myfile)
        with open( settings.LOGOFILE_PATH, "wb+") as logof:
            srcf = fs.open( filename, "rb")
            logof.write( srcf.read())
            srcf.close()
            fs.delete(filename)
        uploaded_file_url = fs.url(filename)
        return render(request, 'logo_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'logo_upload.html')