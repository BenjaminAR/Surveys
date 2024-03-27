"""sx_amsamex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.sx_accounts.views import login_view
from django.conf.urls import handler404
from apps.sx_login.views import page_not_found404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='root'),
    path('sx_accounts/', include('apps.sx_accounts.urls'), name='accounts'),
    path('sx_dashboard/', include('apps.sx_dashboard.urls'), name='dashboard'),
    path('sx_login_e/', include('apps.sx_login.urls'), name='login_error'),
    path('', include('apps.sx_surveys.urls'), name='surveys'),
]

handler404 = page_not_found404