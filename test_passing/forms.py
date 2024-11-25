
from django import forms
from django.forms import inlineformset_factory
from .models import Test, Question, Answer
from users.models import Teacher

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'time_of_execute', 'subject_area', 'teacher']
        widgets = {
            'time_of_execute': forms.TextInput(attrs={'placeholder': 'Введите время выполнения в формате HH:MM:SS'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_type', 'text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'correctness_of_answer']

# Formsets
QuestionFormset = inlineformset_factory(
    Test,              # Parent model
    Question,          # Child model
    form=QuestionForm,
    extra=1,           # Add one empty form by default
    can_delete=True,   # Allow deleting questions
)

AnswerFormset = inlineformset_factory(
    Question,         # Parent model
    Answer,           # Child model
    form=AnswerForm,
    extra=1,          # Add one empty form by default
    can_delete=True,  # Allow deleting answers
)

     
