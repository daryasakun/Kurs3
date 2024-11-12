from django.shortcuts import render, redirect
from .forms import UserLoginForm, StudentRegistrationForm
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


#def registration(request):
#    if request.method == 'POST':
#        form = UserRegistrationForm(data=request.POST)
#        if form.is_valid():
#            form.save()
#            return HttpResponseRedirect(reverse('users:login'))
#    else:
#        form = UserRegistrationForm()
#    return render(request, 'users/registration.html')

def registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Сохраняем нового студента в базе данных
            user = form.save()  # Сохраняем студента (объект User)
            # После регистрации можно автоматически войти в систему
            # from django.contrib.auth import login
            # login(request, user)
            return redirect('main:index')  # Перенаправляем на страницу входа
    else:
        form = StudentRegistrationForm()

    return render(request, 'users/registrati.html', {'form': form})

def profile(request):
    return render(request, 'users/profile.html')

def logout(request):
    return render(request, 'users/logout.html')