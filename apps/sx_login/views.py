from django.shortcuts import render

# Create your views here.

def page_not_found404(request, exception):
    return render(request, 'sx_login/404.html' )