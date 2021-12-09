from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

def home(request):
    content = {
        'title': "Home",
        'heading': "Home",
    }
    return render(request, 'todo/home.html', content)

def signup_user(request):
    content = {
        'title': "SignUp",
        'heading': "Sign Up",
        'form': UserCreationForm(),
    }
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', content)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                content['error'] = "User is already exists."
                return render(request, 'todo/signupuser.html', content)
        else:
            content['error'] = "Password didn't match"
            return render(request, 'todo/signupuser.html', content)

def login_user(request):
    content = {
        'title': "Login",
        'heading': "Login",
        'form': AuthenticationForm(),
    }
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', content)
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            content['error'] = "User and password didn't match"
            return render(request, 'todo/loginuser.html', content)
        else:
            login(request, user)
            return redirect('current_todos')

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def current_todos(request):
    content = {
        'title': "ToDo's",
        'heading': " - todo's",
    }
    return render(request, 'todo/currenttodos.html', content)