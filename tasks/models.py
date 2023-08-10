from django.db import models
from django.contrib.auth.models import User # Predeterminado por django para registrar usuarios

# Create your models here.
class Task(models.Model):
	title = models.CharField(max_length = 100)
	description = models.TextField(blank = True)
	created_at = models.DateTimeField(auto_now_add = True)
	date_completed = models.DateTimeField(null = True)
	important = models.BooleanField(default = False)
	user =  models.ForeignKey(User, on_delete = models.CASCADE) # Relacionamos la tabla tasks con la tabla users por el id del usuario. No es necesario poner sufijos _id o Id. django lo hace por nosotros

	def __str__(self):
		return self.title