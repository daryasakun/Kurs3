from django.contrib import admin


from users.models import User
from users.models import Student
from users.models import Teacher

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
