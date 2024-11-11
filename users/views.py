from django.shortcuts import render
from users.forms import UserLoginForm
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    
    context = {
        'title': 'Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def registration(request):
    return render(request, 'users/registration.html')

def profile(request):
    return render(request, 'users/profile.html')

def logout(request):
    return render(request, 'users/logout.html')