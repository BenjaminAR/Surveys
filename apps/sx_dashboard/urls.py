from django.urls import path
from . import views

app_name = 'sx_dashboard'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='sx_dashboard'),
    path('dashboard_asam/', views.dashboard_view_asam, name='sx_dashboard_asam'),
    path('dashboard_amsa/', views.dashboard_view_amsa, name='sx_dashboard_amsa'),
    path('dashboard_pruebas/', views.dashboard_pruebas, name='sx_dashboard_pruebas'),
    path('survey_modal/', views.get_survey_modal, name='get_survey_modal'),
    path('get_survey_modal_amsa/', views.get_survey_modal_amsa, name='get_survey_modal_amsa'),
    path('dowload_csv/', views.download_filtered_data, name='download_filtered_data'),
    path('dowload_pdf/', views.download_filtered_data_pdf, name='dowload_pdf'),

    path('dowload_pdf_amsa/', views.download_filtered_data_pdf_amsa, name='dowload_pdf_amsa'),
    path('descargar_excel/', views.descargar_excel_amsa, name='descargar_excel'),

    # Otras URLs de la aplicación "main" si las tienes
]
