from django.urls import path
from . import views
from .views import export_gist

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_project/', views.create_project, name='create_project'),
    path('project/<uuid:project_id>/', views.view_project, name='view_project'),
    path('project/<uuid:project_id>/add_todo/', views.add_todo, name='add_todo'),
    path('todo/<uuid:todo_id>/toggle/', views.toggle_todo, name='toggle_todo'),
    path('todo/<uuid:todo_id>/remove/', views.remove_todo, name='remove_todo'), 
    path('export_gist/<uuid:project_id>/', export_gist, name='export_gist'), 
]
