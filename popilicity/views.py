from django.shortcuts import render
from api import autoActions

def index(request):
    return render(request, 'index.html')

def test(request):
    autoActions.userPointCalculate(2)
    return render(request, 'index.html')
