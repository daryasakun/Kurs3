from django.shortcuts import render, redirect
from .forms import UserLoginForm, StudentRegistrationForm
from django.contrib import auth
from django.urls import reverse
from django.http import HttpResponseRedirect
from test_passing.models import Test
from django.utils.functional import SimpleLazyObject
from users.models import Teacher, User, Student
from django.core.paginator import Paginator
from django.db.models.functions import Lower
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

    # Поиск и сортировка для преподавателя
    created_search_query = request.GET.get('created_search', '')
    created_sort_order = request.GET.get('created_sort', 'title')  # Сортировка по умолчанию - по названию

    if hasattr(user, 'teacher'):
        created_tests = Test.objects.filter(teacher_id=user.id)

        # Поиск по названию теста
        if created_search_query:
            created_tests = created_tests.filter(title__icontains=created_search_query)

        # Сортировка по полю 'title' без учета регистра
        if created_sort_order == 'title_desc':
            created_tests = created_tests.order_by(Lower('title').desc())
        else:
            created_tests = created_tests.order_by(Lower('title').asc())

        # Пагинация
        created_tests_paginator = Paginator(created_tests, 5)
        created_tests_page_number = request.GET.get('created_page')
        created_tests_page_obj = created_tests_paginator.get_page(created_tests_page_number)
    else:
        created_tests_page_obj = []  # Пустая пагинация для преподавателя

    # Поиск и сортировка для студента
    available_search_query = request.GET.get('available_search', '')
    available_sort_order = request.GET.get('available_sort', 'title')

    if hasattr(user, 'student'):
        available_tests = Test.objects.all()

        # Поиск по названию теста
        if available_search_query:
            available_tests = available_tests.filter(title__icontains=available_search_query)

        # Сортировка по полю 'title' без учета регистра
        if available_sort_order == 'title_desc':
            available_tests = available_tests.order_by(Lower('title').desc())
        else:
            available_tests = available_tests.order_by(Lower('title').asc())

        # Пагинация
        available_tests_paginator = Paginator(available_tests, 5)
        available_tests_page_number = request.GET.get('available_page')
        available_tests_page_obj = available_tests_paginator.get_page(available_tests_page_number)
    else:
        available_tests_page_obj = []  # Пустая пагинация для студента

    context = {
        'user': user,
        'created_tests': created_tests_page_obj,
        'available_tests': available_tests_page_obj
    }
    return render(request, 'users/profile.html', context)