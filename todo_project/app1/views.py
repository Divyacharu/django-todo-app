from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Project, Todo
from .forms import ProjectForm, TodoForm
import os
import requests
from django.conf import settings
from django.http import HttpResponse
@login_required

#def home(request):
    #return render(request, 'home.html')
def home(request):
    projects = Project.objects.filter(user=request.user)  # Only show user’s projects
    print(f"Logged-in User: {request.user}")
    print(f"Projects Found: {projects.count()}")  # Debugging statement
    return render(request, 'projects.html', {'projects': projects})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('home')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})



def view_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    todos = Todo.objects.filter(project=project)
    
    # Count completed tasks
    todos_completed = todos.filter(completed=True).count()
    
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.project = project
            todo.save()
            return redirect('view_project', project_id=project.id)
    else:
        form = TodoForm()

    return render(request, 'project_todos.html', {
        'project': project,
        'todos': todos,
        'todos_completed': todos_completed,
        'form': form,
    })

def add_todo(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.project = project
            todo.save()
    return redirect('view_project', project_id=project.id)

def toggle_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.completed = not todo.completed  # Toggle status
    todo.save()
    return redirect('view_project', project_id=todo.project.id)

def remove_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    project_id = todo.project.id  # Get associated project ID
    todo.delete()
    return redirect('view_project', project_id=project_id) 

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


@login_required
def export_gist(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    todos = Todo.objects.filter(project=project)

    # Prepare Summary Content
    summary_content = f"# {project.title} - Todo Summary\n\n"
    summary_content += f"✅ Completed: {todos.filter(completed=True).count()} / {todos.count()} Tasks\n\n"

    for todo in todos:
        status = "✔️" if todo.completed else "❌"
        summary_content += f"- {status} **{todo.task}** - {todo.description}\n"

    # **1️⃣ Save as Local Markdown File**
    local_filename = f"{project.title.replace(' ', '_')}_summary.md"
    local_filepath = os.path.join(settings.MEDIA_ROOT, local_filename)

    with open(local_filepath, "w", encoding="utf-8") as file:
        file.write(summary_content)

    # **2️⃣ Upload to GitHub Gist**
    response = requests.post(
        "https://api.github.com/gists",
        headers={"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"},
        json={
            "description": f"Todo Summary for {project.title}",
            "public": False,  # Secret Gist
            "files": {local_filename: {"content": summary_content}},
        },
    )

    if response.status_code == 201:
        gist_url = response.json().get("html_url")

        # **Return a Download Response for the Local File**
        with open(local_filepath, "rb") as file:
            response = HttpResponse(file.read(), content_type="text/markdown")
            response["Content-Disposition"] = f'attachment; filename="{local_filename}"'
            return response  # User will download the markdown file after exporting

    else:
        return render(request, "error.html", {"error": "Failed to create gist."})
