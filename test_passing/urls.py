from django.urls import path
from . import views

app_name = 'test_passing'

urlpatterns = [
    path('create-test/', views.create_test, name='create_test'),
    path('test/<int:test_id>/create-question/', views.create_question, name='create_question'),
    path('question/<int:question_id>/create-answer/', views.create_answer, name='create_answer'),
    path('test/<int:pk>/edit/', views.edit_test, name='edit_test'),
    path('question/<int:pk>/delete/', views.delete_question, name='delete_question'),
    path('test/<int:pk>/', views.test_detail, name='test_detail'),
    path('test/start/<int:test_id>/', views.start_test, name='start_test'),
    path('test/<int:session_id>/execution/',  views.test_execution, name='test_execution'),
    path('test/<int:session_id>/completion/',  views.test_completion, name='test_completion'),
    path('test/expired/',  views.test_expired, name='test_expired'),
    path('test/<int:session_id>/submit/', views.submit_answer, name='submit_answer'),
    path('start_test/<int:test_id>/', views.test_start, name='test_start'),
    
]
