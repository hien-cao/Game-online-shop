from django.shortcuts import render
from django.http import HttpResponse

from .contexts import home_context

# Create your views here.
def home(request):
    if request.user.is_authenticated == True:
        print('Do redirect to browse')
        # HttpResponseRedirect(...)
    context = {
        **home_context,
    }
    print(context)
    return HttpResponse('Hello world!')

def terms_and_conditions(request):
    return HttpResponse('Terms and conditions')