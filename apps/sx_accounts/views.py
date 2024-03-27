# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomUserEditForm, CustomUserDeleteForm
from .models import CustomUser

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('sx_dashboard:sx_dashboard')  # Redirige al usuario a main/dashboard/
        else:
            error_message = 'Credenciales inválidas. Inténtalo nuevamente.'
            return render(request, 'sx_accounts/login.html', {'error_message': error_message})
    else:
        return render(request, 'sx_accounts/login.html')

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def create_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sx_accounts:manage_users')  # Redirige a la página principal después de crear un usuario exitosamente
    else:
        form = CustomUserCreationForm()
    return render(request, 'sx_accounts/create_user.html', {'form': form})

@user_passes_test(is_admin)
def manage_users_view(request):
    users = CustomUser.objects.all()  # Obtiene todos los usuarios
    return render(request, 'sx_accounts/manage_users.html', {'users': users})

@user_passes_test(is_admin)
def edit_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('sx_accounts:manage_users')
    else:
        form = CustomUserEditForm(instance=user)
    return render(request, 'sx_accounts/edit_user.html', {'form': form, 'user': user})

@user_passes_test(is_admin)
def delete_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserDeleteForm(request.POST)
        if form.is_valid():
            # Elimina al usuario
            user.delete()
            return redirect('sx_accounts:manage_users')  # Redireccionar a la página de administración después de la eliminación
        else:
            return JsonResponse({'success': False})  # Devuelve una respuesta JSON con error si el formulario no es válido
    else:
        form = CustomUserDeleteForm(initial={'user_id': user_id})
    return render(request, 'sx_accounts/delete_user.html', {'form': form, 'user': user})