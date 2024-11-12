from django import forms
from django.contrib.auth.forms import AuthenticationForm
from users.models import User
from users.models import Student
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class UserLoginForm(AuthenticationForm):

    #username = forms.CharField(
    #    label = 'Имя',
    #    widget=forms.TextInput(attrs={"autofocus": True, 
    #                                'class': 'form-control',
    #                                'placeholder': 'Введите ваше имя пользователя'})
    #)
    #password = forms.CharField(
    #    label = 'Пароль',
    #    widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
    #                                      'class': 'form-control',
    #                                      'placeholder': 'Введите ваш пароль'})
    #)

    class Meta:
        model = User
        fields = ['username', 'password']

    username = forms.CharField()
    password = forms.CharField()


#class UserRegistrationForm(UserCreationForm):
#    model = Student
#    fields = (
#        "full_name",
#       "email",
#        "phone_number",
#        "group_number",
#        "direction_of_training",
#        "password1",
#        "password2",
#    )
#    full_name = forms.CharField()
#    email = forms.CharField()
#    phone_number = forms.CharField()
#    group_number = forms.CharField()
#    direction_of_training = forms.CharField()
#    password1 = forms.CharField()
#    password2 = forms.CharField()
#    username = email

class StudentRegistrationForm(UserCreationForm):
    # Дополнительные поля для модели Student
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    phone_number = forms.CharField(max_length=15, required=False)
    group_number = forms.CharField(max_length=20)
    direction_of_training = forms.CharField(max_length=50)
    #username = email

    class Meta:
        model = Student  # Модель User или Student, в зависимости от настроек
        fields = ('email', 'full_name', 'phone_number', 'password1', 'password2', 'group_number', 'direction_of_training')