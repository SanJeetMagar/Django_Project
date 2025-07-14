from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Todo
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserForm, TodoForm



@login_required
def todo_list(request):
    todos = Todo.objects.all() 
    return render(request, 'todo/todo_list.html', {'todos': todos})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = User.objects.filter(username = username).first()

        if user and user.check_password(password):
            login(request,user)
            return redirect ("todo_list")
        else:
            messages.error(request,"Invalid Username or Password")

            render(request, "todo/registration/login.html")
    return render(request, "todo/registration/login.html")

def signup_page(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")

            if User.objects.filter(username=username).exists():
                return HttpResponse("User already exits") 
            if username and password and email:
                user = User.objects.create_user(username=username, password=password, email=email)
                return redirect("login")
        else:
            return HttpResponse("Invalid form submission")   
    form = UserForm()
    return render (request, "todo/signup.html", {"form": form})             






@login_required
def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if title:
           
            Todo.objects.create(
                title=title,
                description=description
            )
            messages.success(request, 'Todo added successfully!')
            return redirect('todo_list')
        else:
            messages.error(request, 'Title is required!')
    
    return render(request, 'todo/add_todo.html')

@login_required
def edit_todo(request, todo_id):
    """Edit an existing todo"""
    todo = get_object_or_404(Todo, id=todo_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        completed = request.POST.get('completed') == 'on'
        
        if title:
            todo.title = title
            todo.description = description
            todo.completed = completed
            todo.save()
            messages.success(request, 'Todo updated successfully!')
            return redirect('todo_list')
        else:
            messages.error(request, 'Title is required!')
    
    return render(request, 'todo/edit_todo.html', {'todo': todo})

@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo deleted successfully!')
        return redirect('todo_list')
    
    return render(request, 'todo/delete_todo.html', {'todo': todo})

@login_required
def complete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.completed = True
    todo.save()
    messages.success(request, 'Todo marked as completed!')
    return redirect('todo_list')