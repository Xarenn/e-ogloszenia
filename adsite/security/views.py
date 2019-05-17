from django.shortcuts import render, redirect
from .register_form import RegisterForm
from .details_form import DetailsForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})

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
    return render(request, 'auth/change_password.html', {'form': form })

def show_details(request):
    return render(request, 'details.html')

def edit_details(request):
    if request.method == 'POST':
           form = DetailsForm(request.POST, instance=request.user)
           if form.is_valid():
               form.save()
               return redirect('show_details')
    else:
        form = DetailsForm(instance=request.user)
    return render(request, 'edit_details.html', {'form': form})
         
