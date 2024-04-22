from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate, login
from .forms import CreationForm, LoginForm, UpdateForm
from django.contrib import messages
from .models import User
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

def register_user(request):
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)  # Log in the user after registration
            messages.add_message(request, messages.SUCCESS, f'Thanks for registering {user.username}.')
            return redirect('accounts:login')  # Redirect to the home page or any other page you want
    else:
        form = CreationForm()

    return render(request, 'accounts/registration/registration.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'pages:index')
                messages.add_message(request, messages.SUCCESS, f'Welcome back {user.username}')
                return redirect(next_url)  # Redirect to the home page or any other page you want
            else:
                messages.add_message(request, messages.ERROR, 'Invalid Credentials. Login Unsuccessful. Contact Admin')
    else:
        form = LoginForm()

    return render(request, 'accounts/registration/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, f'See you soon {request.user.username}')
    return redirect('pages:index')