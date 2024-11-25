from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from users.models import User
from users.models import Student
from users.models import Teacher

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'full_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

@admin.register(Student)
class StudentAdmin(CustomUserAdmin):
    model = Student
    list_display = ('email', 'full_name', 'group_number', 'direction_of_training', 'is_active')

@admin.register(Teacher)
class TeacherAdmin(CustomUserAdmin):
    model = Teacher
    list_display = ('email', 'full_name', 'post', 'is_active')