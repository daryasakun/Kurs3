from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    #path('registration/', views.registration, name='registration'),
    path('registration/', views.registration, name='registration'),

    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]
