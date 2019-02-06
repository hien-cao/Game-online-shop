from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect


def e500(request, **kwargs):
    return render(request, 'error.html', status=500, **kwargs)


def e404(request, **kwargs):
    return render(request, 'error.html', status=500, **kwargs)


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('games')
    return render(request, 'home.html', {'nopad': True})


def terms_and_conditions(request):
    return HttpResponse('Terms and conditions')
