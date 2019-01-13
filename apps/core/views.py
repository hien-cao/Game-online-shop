from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.user.is_authenticated == True:
        print('Do redirect to browse')
        # HttpResponseRedirect(...)
    context = {'home': 'is-active'}
    return HttpResponse('Hello world!')

def terms_and_conditions(request):
    return HttpResponse('Terms and conditions')