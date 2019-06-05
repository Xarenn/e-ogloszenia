from django.shortcuts import render, redirect
from .register_form import RegisterForm
from .details_form import DetailsForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from .token_generator import account_activation_token
from .models import User
from .serializers import UserSerializer
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import requests 
from . import api_urls
import json


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            email = form.cleaned_data.get('email')
            _send_activation_mail(email, user, get_current_site(request))
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})


@login_required
def show_details(request):
    return render(request, 'details.html')


@login_required
def edit_details(request):
    if request.method == 'POST':
        form = DetailsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('show_details')
    else:
        form = DetailsForm(instance=request.user)
    return render(request, 'edit_details.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        response = requests.post(api_urls.REGISTER_USER, json=serializer.data)
        data = json.loads(response.text)
        user.server_id = data['id']
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def _send_activation_mail(email: str, user: User, current_site):
    message = render_to_string('registration/email_acc.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    send_mail(
        'Account Activation',
        message,
        'addservice@op.pl',
        [email],
        fail_silently=False,
    )
