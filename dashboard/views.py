from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, 'dashboard/home.html')

def faculty(request):
    return render(request, 'dashboard/faculty.html')

def cadet(request):
    return render(request, 'dashboard/cadet.html')