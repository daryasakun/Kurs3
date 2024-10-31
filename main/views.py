from django.http import HttpResponse
from django.shortcuts import render

#контроллер
def index(request):
    return render(request, 'main/index.html')

