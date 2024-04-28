from django.contrib.auth import login, authenticate
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import SignUpForm, UserLoginForm
from tasks.models import Task

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    print("request", request)
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        print("form", form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print("user", user)
            if user is not None:
                login(request, user)
                return redirect('home') 
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})