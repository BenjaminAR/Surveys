from django.urls import path
from . import views

app_name = 'sx_login'

urlpatterns = [
    path('404/', views.page_not_found404, name='404'),

]
