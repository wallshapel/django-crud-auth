from django.contrib import admin
from .models import Task

# Register your models here.
admin.site.register(Task) # Inluimos el modelo de tareas en el panel de administración
