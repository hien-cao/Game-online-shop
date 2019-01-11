from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

from .forms import RegisterForm
from .utils.tokens import account_activation_token

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            subject = 'Activate your account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = RegisterForm()
    return render(request, 'register.html', { 'form': form })

@login_required(login_url='/login/')
def welcome(request):
    return HttpResponse('Welcome!')

def account_activation_sent(request):
    messages.info(
        request,
        'We have sent you a verification link. Please check your email.'
    )
    return redirect('login')

def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend=backend)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')
