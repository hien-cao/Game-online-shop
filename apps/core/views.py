from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .contexts import home_context

# Create your views here.
def home(request):
    if request.user.is_authenticated == True:
        return HttpResponseRedirect('games')
    context = {
        **home_context,
    }
    return HttpResponse('Hello world!')

def terms_and_conditions(request):
    return HttpResponse('Terms and conditions')
