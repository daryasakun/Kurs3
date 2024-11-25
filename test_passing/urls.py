from django.urls import path
from . import views

app_name = 'test_passing'

urlpatterns = [
    path('create-test/', views.create_test, name='create_test'),
    path('test/<int:test_id>/create-question/', views.create_question, name='create_question'),
    path('question/<int:question_id>/create-answer/', views.create_answer, name='create_answer'),
    path('test/<int:pk>/edit/', views.edit_test, name='edit_test'),
    path('question/<int:pk>/delete/', views.delete_question, name='delete_question'),
    path('test/<int:pk>/', views.test_detail, name='test_detail')
    
]
