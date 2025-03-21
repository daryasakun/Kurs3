from django.db import models
from users.models import Student
from test_passing.models import Test, TestSession

class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    number_of_points = models.IntegerField()
    date_of_passing = models.DateTimeField(auto_now_add=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test_session = models.ForeignKey(TestSession, on_delete=models.CASCADE, null=True, blank=True)  # Связь с тестовой сессией

    class Meta:
        db_table = 'results'
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

