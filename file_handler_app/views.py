from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def test(request):
    print("testing the view")
    return HttpResponse('testing the views')

def show_files(request):
    return render(request, 'file_loader.html')
