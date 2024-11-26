from django.db import models
from users.models import Student
# Create your models here.



class Test(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    time_of_execute = models.DurationField(null=True, blank=True)
    subject_area = models.CharField(max_length=50)
    from users.models import Teacher
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'test'
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    question_type = models.CharField(max_length=50)  
    text = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    class Meta:
        db_table = 'question'
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    text = models.TextField()
    correctness_of_answer = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        db_table = 'answer'
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class TestSession(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'test')


class TestAnswer(models.Model):
    test_session = models.ForeignKey(TestSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('test_session', 'question')