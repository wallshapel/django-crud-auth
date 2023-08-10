from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('signup/', views.signup, name = 'signup'),
    path('logout/', views.close, name = 'logout'),
    path('login/', views.enter, name = 'login'),
    path('tasks/', views.tasks, name = 'tasks'),
    path('task/<int:id>/', views.task, name = 'task'),
    path('task/<int:id>/completed', views.completed, name = 'completed'),
    path('task/<int:id>/delete', views.delete, name = 'delete'),
    path('tasks/create/', views.create_task, name = 'create_task'),
     path('tasks/completed/', views.tasks_completed, name = 'tasks_completed')
]
