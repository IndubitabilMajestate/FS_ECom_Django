from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Logged in succesfully!"))
            return redirect('home')
        else:
            messages.success(request, ("Error logging in. Try again."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ("Logged out. Thanks for shopping!"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            
            user = authenticate(username=username,password=password)
            login(request, user)
            messages.success(request, ("Successful registration."))
            return redirect('home')
        else:
            messages.success(request, ("Problem registering."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})

