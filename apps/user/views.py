import pytz
from datetime import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .forms import SignUpForm
from .utils.tokens import account_activation_token

from ..game.models import Game


def signup(request):
    """
    Display the sign up view.

    **Template:**
    :template:`signup.html`
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Store to DB after is_active is set to False.
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # Create "an email" by populating the template
            # with given arguments:
            # - use user to greet
            # - use other args to construct URI
            subject = 'Activate your account'
            message = render_to_string(
                'account_activation_email.html',
                {
                    'user':
                    user,
                    'domain':
                    get_current_site(request).domain,
                    # encode
                    'uid':
                    force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                    'token':
                    account_activation_token.make_token(user),
                })
            # Send email.
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def signout(request):
    """Sign out the user."""
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    context = {}
    now = datetime.now(pytz.utc)
    game_list = Game.objects.filter(created_by=request.user.profile)
    purchased_games = request.user.profile.purchases.filter(purchased_at__isnull=False).order_by('-purchased_at')
    # Add purchased games to the context
    if len(purchased_games) != 0:
        context['purchased_games'] = purchased_games
    # as html forms only support POST, patching is done via this method
    if request.method == 'POST':
        for key in request.POST:
            if hasattr(request.user.profile, key):
                setattr(request.user.profile, key, request.POST[key])

        request.user.profile.save(update_fields=[
            key for key in request.POST if hasattr(request.user.profile, key)
        ])
    if request.user.is_authenticated:
        # Query for the statistics data 
        if len(game_list) != 0:
            total_revenue = 0
            total_purchases = 0
            year_purchases = 0
            month_purchases = 0
            for game in game_list:
                total_revenue += game.price * game.purchases.filter(purchased_at__isnull=False).count()
                total_purchases += game.purchases.filter(purchased_at__isnull=False).count()
                year_purchases += len(game.purchases.filter(purchased_at__year=now.year))
                month_purchases += len(game.purchases.filter(purchased_at__year=now.year, purchased_at__month=now.month))

            statistics = {
                'number_of_games': len(game_list),
                'total_revenue': total_revenue,
                'purchase': {
                    'total_purchases': total_purchases,
                    'current_year_purchases': year_purchases,
                    'current_month_purchases': month_purchases
                }
            }
            context['statistics'] = statistics
        else:
            context['message'] = 'You have not uploaded any game'
    return render(request, 'profile/profile.html', context)


def account_activation_sent(request):
    """
    Display an info message for verifying email address.

    **Template:**
    :template:`user/signin`
    """
    messages.info(
        request,
        'We have sent you a verification link. Please check your email.')
    return redirect('signin')


def activate(request,
             uidb64,
             token,
             backend='django.contrib.auth.backends.ModelBackend'):
    """Activate the user, confirm that the email is verified."""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # decode
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
