from django.urls import path
from . import views

app_name = 'sx_dashboard'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='sx_dashboard'),
    path('dashboard_asam/', views.dashboard_view_asam, name='sx_dashboard_asam'),
    path('dashboard_pruebas/', views.dashboard_pruebas, name='sx_dashboard_pruebas'),
    path('survey_modal/', views.get_survey_modal, name='get_survey_modal'),
    path('dowload_csv/', views.download_filtered_data, name='download_filtered_data'),
    path('dowload_pdf/', views.download_filtered_data_pdf, name='dowload_pdf'),

    # Otras URLs de la aplicación "main" si las tienes
]
