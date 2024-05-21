from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import *
from .models import Encuesta, Agencias, Encuesta_automotores
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils import timezone


def index(request):
    return render(request, 'sx_surveys/index.html')

def encuesta_create_view_msa(request):
    if request.method == 'POST':
        agencia = get_object_or_404(Agencias, id=1)
        form = EncuestaFormMitsu(request.POST, initial={'agencia': agencia.id})
        form.fields['agencia'].disabled = True
        if form.is_valid():
            form.save()
            return redirect('/succesesc/')
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    else:
        form = EncuestaFormMitsu()

    return render(request, 'sx_surveys/surveys_msa.html', {'form': form})

def encuesta_create_view_asam(request):
    if request.method == 'POST':
        agencia = Agencias.objects.get(id=2)
        encuesta = Encuesta(agencia=agencia)
        form = EncuestaFormMitsu(request.POST, instance=encuesta)
        form.fields['agencia'].disabled = True
        if form.is_valid():
            print(encuesta.agencia)
            form.save()
            return redirect('/succesesc/')
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    else:
        form = EncuestaFormMitsu()

    return render(request, 'sx_surveys/surveys_asam.html', {'form': form})

def encuesta_create_view_amsa(request):
    if request.method == 'POST':
        agencia = Agencias.objects.get(id=3)
        encuesta = Encuesta_automotores(agencia=agencia)
        form = EncuestaFormAmsa(request.POST, instance=encuesta)
        form.fields['agencia'].disabled = True
        if form.is_valid():
            print(encuesta.agencia)
            form.save()
            return redirect('/succesesc/')
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    else:
        form = EncuestaFormAmsa()

    return render(request, 'sx_surveys/surveys_amsa.html', {'form': form})

def succesesc(request):
    return render(request, 'sx_surveys/succesesc.html')

def get_survey(request):
    if request.method == 'POST':
        numero_orden = request.POST.get('numero_orden')
        try:
            encuesta = Encuesta.objects.get(numero_orden=numero_orden)
            return render(request, 'sx_surveys/get_order.html', {'encuesta': encuesta})
        except Encuesta.DoesNotExist:
            mensaje_error = "No se encontró ninguna encuesta con el número de orden proporcionado."
            return render(request, 'sx_surveys/get_order.html', {'mensaje_error': mensaje_error})
    else:
        return render(request, 'sx_surveys/get_order.html') 
    
