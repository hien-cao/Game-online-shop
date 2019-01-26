from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect


def e500(request):
    response = render_to_response('error.html')
    response.status_code = 500
    return response


def e404(request):
    response = render_to_response('error.html')
    response.status_code = 404
    return response


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('games')
    return render(request, 'home.html', {'nopad': True})


def terms_and_conditions(request):
    return HttpResponse('Terms and conditions')
