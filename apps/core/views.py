from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect


def e500(request, **kwargs):
    """View for displaying 500 error page."""
    return render(request, 'error.html', status=500, **kwargs)


def e404(request, **kwargs):
    """View for displaying 404 error page."""
    return render(request, 'error.html', status=404, **kwargs)


def home(request):
    """View for Home page."""
    if request.user.is_authenticated:
        return HttpResponseRedirect('games')
    return render(request, 'home.html', {'nopad': True})


def terms_and_conditions(request):
    """View for displaying Terms and Conditions."""
    # NOTE: As Terms and Conditions are out of scope
    # for this scope, we do not implement these.
    # In a real application this would be mandatory.
    return HttpResponse('Terms and conditions')
