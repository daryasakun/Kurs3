from django.shortcuts import render, redirect
from .forms import UserLoginForm, StudentRegistrationForm
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponseRedirect
from test_passing.models import Test
from django.utils.functional import SimpleLazyObject
from users.models import Teacher, User, Student

from django.contrib.auth.decorators import login_required
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
                return HttpResponseRedirect(reverse('users:profile'))
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



def logout(request):
    return render(request, 'users/logout.html')

@login_required
def user_profile(request):
    user = request.user
    #print(isinstance(user, Student))
    


    # Если это преподаватель, то получаем его тесты
    if hasattr(user, 'teacher'):
        created_tests = Test.objects.filter(teacher_id=user.id)
        print(f"Created tests: {created_tests}")
    else:
        created_tests = []

    if hasattr(user, 'student'):
        created_tests = Test.objects.all()  # Все тесты

    context = {
        'user': user,
        'created_tests': created_tests
    }
    return render(request, 'users/profile.html', context)