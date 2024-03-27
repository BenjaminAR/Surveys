from django.urls import include, path
from . import views
from .views import *

app_name = 'sx_surveys'

urlpatterns = [
    path('', views.index, name='index'),
    path('succesesc/', succesesc, name='succesesc'),
    path('surveys_msa/', encuesta_create_view_msa, name='surveys_msa'),
    path('surveys_asam/', encuesta_create_view_asam, name='surveys_asam'),
    path('surveys_amsa/', encuesta_create_view_msa, name='surveys_amsa'), 
    path('get_survey/', get_survey, name='get_survey'),
]
