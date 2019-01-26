from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('games')
    return render(request, 'home.html')


def terms_and_conditions(request):
    return HttpResponse('Terms and conditions')
