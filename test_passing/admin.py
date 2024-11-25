from django.contrib import admin
from test_passing.models import Test, Answer, Question
# Register your models here.
admin.site.register(Test)
admin.site.register(Answer)
admin.site.register(Question)