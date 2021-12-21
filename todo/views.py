from django import contrib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import tasktodo

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

def create_todos(request):
    content = {
        'title': "TodoCreate",
        'heading': "Create new todo",
        'form': TodoForm(),
    }
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', content)
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('current_todos')
        except ValueError:
            content['error'] = "Bad data passed in"
            return render(request, 'todo/createtodo.html', content)

def current_todos(request):
    todos = tasktodo.objects.filter(user = request.user)
    
    content = {
        'title': "ToDo's",
        'heading': " - todo's",
        'todos': todos,
    }
    return render(request, 'todo/currenttodos.html', content)

def view_todo(request, todo_pk):
    todo = get_object_or_404(tasktodo, pk=todo_pk, user=request.user)
    content = {'todo': todo}
    if request.method == "GET":
        form = TodoForm(instance=todo)
        content['form'] = form
        return render(request, 'todo/tododetail.html', content)
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            content['error'] = 'Bad info'
            return render(request, 'todo/tododetail.html', content)
