from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from django.conf import settings
import os

# Create your views here.
def test(request):
    print("testing the view")
    return HttpResponse('testing the views')

def _get_existing_uploaded_files():
    """ Method to return all the uploaded Files
    """
    uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    root, dirs, files = os.walk(uploads_dir).__next__()
    return files


def show_files(request):
    existing_uploaded_files = _get_existing_uploaded_files()
    return render(request, 'file_loader.html', {'existing_files': existing_uploaded_files})
