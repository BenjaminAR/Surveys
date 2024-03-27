from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'sx_accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create_user/', views.create_user_view, name='create_user'), # Crear un nuevo usuario
    path('manage_users/', views.manage_users_view, name='manage_users'),  # Manipular usuarios extistentes
    path('edit_user/<int:user_id>/', views.edit_user_view, name='edit_user'),  # Editar usuarios existentes
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),  # Eliminación de usuarios
]
