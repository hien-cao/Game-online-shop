from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse('Hello world!')

def terms_and_conditions(request):
    return HttpResponse('Terms and conditions')