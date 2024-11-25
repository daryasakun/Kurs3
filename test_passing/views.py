from django.shortcuts import render, redirect, get_object_or_404
from .forms import TestForm, QuestionFormset, AnswerFormset
from .models import Test, Question, Answer
from users.models import Teacher
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Декоратор для проверки, что пользователь авторизован и является преподавателем
@login_required
def create_test(request):
    # Проверяем, является ли пользователь преподавателем
    try:
        teacher = Teacher.objects.get(email=request.user.email)
    except Teacher.DoesNotExist:
        raise PermissionDenied("Вы не являетесь преподавателем, доступ к созданию тестов запрещен.")

    if request.method == 'POST':
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            test = test_form.save(commit=False)
            test.teacher = teacher  # Устанавливаем текущего преподавателя
            test.save()

            # После создания теста перенаправляем на страницу добавления вопросов
            return redirect('test_passing:create_question', test_id=test.id)
    else:
        test_form = TestForm()

    return render(request, 'test_passing/create_test.html', {'form': test_form})

@login_required
def create_question(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    # Проверяем, является ли текущий пользователь преподавателем этого теста
    if test.teacher != request.user.teacher:
        raise PermissionDenied("У вас нет прав редактировать этот тест.")

    if request.method == 'POST':
        question_formset = QuestionFormset(request.POST, instance=test)
        if question_formset.is_valid():
            question_formset.save()
            return redirect('test_passing:create_question', test_id=test.id)
    else:
        question_formset = QuestionFormset(instance=test)

    # Получаем все вопросы с их ответами
    questions_with_answers = [
        {
            "question": question,
            "answers": Answer.objects.filter(question=question)
        }
        for question in test.question_set.all()
    ]

    return render(request, 'test_passing/create_question.html', {
        'formset': question_formset,
        'test': test,
        'questions_with_answers': questions_with_answers,  # Передаем данные в шаблон
    })

@login_required
def create_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    # Проверяем, является ли текущий пользователь преподавателем этого теста
    if question.test.teacher != request.user.teacher:
        raise PermissionDenied("У вас нет прав редактировать этот вопрос.")

    if request.method == 'POST':
        answer_formset = AnswerFormset(request.POST, instance=question)
        if answer_formset.is_valid():
            # Сохраняем только заполненные формы
            for form in answer_formset:
                if form.cleaned_data:  # Проверяем, что форма не пустая
                    form.save()
            return redirect('test_passing:create_answer', question_id=question.id)
    else:
        answer_formset = AnswerFormset(instance=question)

    return render(request, 'test_passing/create_answer.html', {
        'formset': answer_formset,
        'question': question
    })


@login_required
def edit_test(request, pk):
    test = get_object_or_404(Test, pk=pk)

    # Проверяем, является ли пользователь преподавателем, связанным с тестом
    if not hasattr(request.user, 'teacher') or test.teacher != request.user.teacher:
        raise PermissionDenied("У вас нет прав редактировать этот тест.")
    
    if request.method == 'POST':
        form = TestForm(request.POST, instance=test)
        question_formset = QuestionFormset(request.POST, instance=test)
        if form.is_valid() and question_formset.is_valid():
            form.save()
            question_formset.save()
            return redirect('test_passing:test_detail', pk=test.pk)  # Редирект на страницу теста
    else:
        form = TestForm(instance=test)
        question_formset = QuestionFormset(instance=test)
    
    return render(request, 'test_passing/edit_test.html', {
        'form': form,
        'question_formset': question_formset,
        'test': test,
    })


@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    test = question.test

    # Проверяем, что пользователь является преподавателем теста
    if not hasattr(request.user, 'teacher') or test.teacher != request.user.teacher:
        raise PermissionDenied("У вас нет прав удалять вопросы из этого теста.")

    question.delete()  # Удаляем вопрос
    return redirect('test_passing:edit_test', pk=test.pk)


def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    return render(request, 'test_passing/test_detail.html', {'test': test})

