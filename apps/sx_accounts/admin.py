# accounts/admin.py

from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')  # Campos a mostrar en la lista de usuarios
    search_fields = ('username', 'email')  # Campos por los que se puede buscar
    list_filter = ('is_staff', 'is_superuser')  # Filtros disponibles en el panel

# Registra el modelo CustomUser con la clase CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
