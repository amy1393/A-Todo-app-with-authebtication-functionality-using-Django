from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import create_todoform
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):

    return render(request, "home.html")




def signupuser(request):

    if request.method == "GET":
        return render(request, "signup.html", {'form': UserCreationForm()})

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)

                return redirect('currenttodos')



            except IntegrityError:
                return render(request, "signup.html", {'form': UserCreationForm(), 'error': 'This username already exists'})


            
            

        else:
            return render(request, "signup.html", {'form': UserCreationForm(), 'error': 'Password did not match'})

@login_required(login_url='/login/')
def currenttodos(request):
    todos = Todo.objects.filter(user = request.user, date_on_completed__isnull = True)
    return render(request, 'currenttodos.html', {'todos' : todos})

@login_required(login_url='/login/')
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')    



def loginuser(request):
    if request.method == "GET":
        return render(request, "login.html", {'form': AuthenticationForm()})

    else:
        user = authenticate(username = request.POST['username'], password = request.POST['password'])

        if user is None:
            return render(request, "login.html", {'form': AuthenticationForm(), 'error': 'username or password is incorrect' })

        else:
            login(request,user)
            return redirect('currenttodos')


@login_required(login_url='/login/')
def create_todos(request):
    if request.method == "GET":
        return render(request, "create_todos.html", {'form': create_todoform()})

    else:
        try:
            form = create_todoform(request.POST)
            new_obj = form.save(commit=False)
            new_obj.user = request.user
            new_obj.save()
            return redirect('currenttodos')

        except ValueError:
            return render(request, "create_todos.html", {'form': create_todoform(), 'error' : "Maximum length exceeded"})

@login_required(login_url='/login/')
def view_todo(request, view_todo):
    todo = get_object_or_404(Todo, pk=view_todo, user = request.user)
    if request.method == "GET":
        form = create_todoform(instance = todo)
        return render(request, "view.todo.html", {'todo': todo, 'form': form})

    else:
        try:
            form = create_todoform(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')

        except ValueError:
            return render(request, "view.todo.html", {'todo': todo, 'form': form, 'error': "Bad Input"})

@login_required(login_url='/login/')
def complete(request, complete_todo):
        todo = get_object_or_404(Todo, pk=complete_todo, user = request.user)
        if request.method == "POST":
            todo.date_on_completed = timezone.now()
            todo.save()
            return redirect('currenttodos')

@login_required(login_url='/login/')
def delete(request, deleted_todo):
        todo = get_object_or_404(Todo, pk=deleted_todo, user = request.user)
        if request.method == "POST":
            todo.delete()
            return redirect('currenttodos')


@login_required(login_url='/login/')
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, date_on_completed__isnull=False).order_by('-date_on_completed')
    return render(request, 'completedtodos.html', {'todos' : todos})


    
        

        


