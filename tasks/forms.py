from django.forms import ModelForm # Permite crear formularios a partir de modelos
from .models import Task

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ['title', 'description', 'important'] # Incluyo los campos que me interesen
