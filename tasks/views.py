from django.shortcuts import render, redirect, get_object_or_404 # 'get_object_or_404' sirve para obtener un único registro que cumple ciertos criterios, pero no tumba el servidor si no lo encuentra
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # Estas son clases de django. Una para crear usuarios, la otra para autenticarlos
from django.contrib.auth.models import User # Predeterminado por django para registrar usuarios
from django.contrib.auth import login, logout, authenticate # 'login' no es para verificar si el usuario y contraseña son correctos, si no para logear al usuario, para eso está 'authenticate'
from .forms import TaskForm
from .models import Task
from django.utils import timezone # Necesario para trabajar con fechas
from django.contrib.auth.decorators import login_required # Este decorador servirá como middleware para proteger las rutas si no se está logueado

def home(request):
	return render(request, 'home.html')

def signup(request):
	if request.method == 'GET':
		return render(request, 'signup.html', {
			'form': UserCreationForm # Le pasamos al template un formulario predeterminado de django
		})
	elif request.method == 'POST':
		if request.POST['password1'] == request.POST['password2']:
			# print(request.POST)
			# print('getting data')
			try:
				user = User.objects.create_user(
					username = request.POST['username'],
					password = request.POST['password1'])
				user.save()	
				login(request, user) # Loguea al usuarios mediante una cookie
				# return HttpResponse('User created successfully')
				return redirect('tasks')
			except Exception as e:
				return render(request, 'signup.html', {
					'form': UserCreationForm,
					'error': str(e)
				})			
		else:
			return render(request, 'signup.html', {
				'form': UserCreationForm,
				'error': 'Passwords do not match'
			})				

@login_required
def tasks(request):
	tasks = Task.objects.filter(user = request.user) # Filtra las tareas por el usuario logueado
	return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def close(request): # No puede llamarse 'logout' porque entraría en conflicto con la importación
	logout(request)
	return redirect('home')

def enter(request): # No puede llamarse 'login' porque entraría en conflicto con la importación
	if request.method == 'GET':
		return render(request, 'login.html', {
			'form': AuthenticationForm	
		})
	elif request.method == 'POST':
		user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
		if user is None: # Si no encontró al usuario
			return render(request, 'login.html', {
				'form': AuthenticationForm,
				'error': 'Invalid credentials'
			})
		else:
			login(request, user) # Si el usuarios es válido entonces lo logueamos
			return redirect('tasks') # ... y lodirigimos a la sección de tareas

@login_required
def create_task(request):
	if request.method == 'GET':
		return render(request, 'create_task.html', {
			'form': TaskForm
		})
	elif request.method == 'POST':
		try:
			form = TaskForm(request.POST) # Así pasamos los valores de cada uno de los campos. Sin embargo no viene el usuario. el usuario toca rescatarlo de la sesión con cookie
			new_task = form.save(commit = False) # Preguardado. no guardamos el registro aún.
			new_task.user = request.user # Nos faltaba la info del usuario. De esta forma la obtenemos desde la cookie
			new_task = form.save()
			return redirect('tasks')			
		except Exception as e:
			return render(request, 'create_task.html', {
			'form': TaskForm,
			'error': str(e)
		})		

@login_required
def task(request, id):
	if request.method == 'GET':
		task = get_object_or_404(Task, pk = id, user = request.user) # Le pasamos el modelo y luego obtenemos la tarea por el id y por el usuario logueado
		form = TaskForm(instance = task) # Con 'instance' pasamos un formulario a la vista con los campos y sus respectivos valores de esta tarea 
		return render(request, 'task.html', {'task': task, 'form': form})
	elif request.method == 'POST':
		try:
			task = get_object_or_404(Task, pk = id, user = request.user) # Buscamos la tarea por el id y el usuario logueado
			form = TaskForm(request.POST, instance = task) # De esta forma actualizamos. el request me trae los datos a actualizar. La instancia es la tarea en su estado viejo
			form.save()
			return redirect('tasks')
		except Exception as e:
			return render(request, 'task.html', {'task': task, 'form': form, 'error': str(e)})	

@login_required
def completed(request, id):
	task = get_object_or_404(Task, pk = id, user = request.user)
	if request.method == 'POST':
		task.date_completed = timezone.now() # Devuelve la fecha y hora actual
		task.save()
		return redirect('tasks')

@login_required
def delete(request, id):
	task = get_object_or_404(Task, pk = id, user = request.user)
	if request.method == 'POST':
		task.delete()
		return redirect('tasks')

@login_required
def tasks_completed(request):
	tasks = Task.objects.filter(user = request.user, date_completed__isnull = False).order_by('-date_completed') # Filtra las tareas siempre y cuando el campo date_completed sea diferente de 'NULL'
	return render(request, 'tasks.html', {'tasks': tasks})