from django.shortcuts import render, redirect, get_object_or_404
from .forms import TestForm, QuestionFormset, AnswerFormset
from .models import Test, Question, Answer, TestSession, TestAnswer
from users.models import Teacher
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from results.models import Result
from django.http import HttpResponseForbidden
from django.utils.timezone import now
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









# Старт теста
# Старт теста
def start_test(request, test_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    if not hasattr(request.user, 'student'):
        return HttpResponseForbidden("Только студенты могут проходить этот тест")

    # Проверяем существование теста
    test = Test.objects.filter(id=test_id).first()
    if not test:
        return HttpResponseForbidden("Тест не найден")

    # Создаем сессию тестирования
    session, created = TestSession.objects.get_or_create(
        student=request.user.student,
        test=test,
        defaults={
            'start_time': now(),
            'end_time': now() + test.time_of_execute,  # Устанавливаем время окончания
        }
    )

    if not created and session.completed:
        return redirect('test_passing:test_completion', session_id=session.id) 

    # Проверьте, истекло ли время выполнения
    if session.end_time < now():
        session.completed = True
        session.save()
        return redirect('test_passing:test_expired')  # Перенаправление на страницу с уведомлением о завершении

    return redirect('test_passing:test_execution', session_id=session.id)

@login_required
def test_execution(request, session_id):
    # Получаем текущую сессию теста
    test_session = get_object_or_404(TestSession, id=session_id, student=request.user.student)

    # Проверяем, не завершен ли тест
    if test_session.completed:
        return redirect('test_passing:test_completion', session_id=session_id)

    # Получаем все вопросы, на которые студент уже ответил
    answered_questions = TestAnswer.objects.filter(test_session=test_session).values_list('question_id', flat=True)

    # Получаем первый вопрос, на который студент еще не ответил
    current_question = Question.objects.filter(test=test_session.test).exclude(id__in=answered_questions).first()

    if current_question:
        context = {
            'test': test_session.test,
            'question': current_question,
            'session_id': session_id,
            'test_session': test_session
        }
        return render(request, 'test_passing/test_execution.html', context)

    # Если вопросов больше нет
    return redirect('test_passing:test_completion', session_id=session_id)

# Завершение теста и подсчет результатов
@login_required
def test_completion(request, session_id):
    # Получаем текущую сессию теста
    test_session = get_object_or_404(TestSession, id=session_id, student=request.user.student)
    
    if not test_session.completed:
        # Если тест еще не завершен, перенаправляем на выполнение
        return redirect('test_passing:test_execution', session_id=session_id)
    
    # Подсчитываем результат
    test = test_session.test
    questions = Question.objects.filter(test=test)
    total_points = 0
    max_points = questions.count()

    for question in questions:
        # Получаем правильный ответ для вопроса
        correct_answer = Answer.objects.filter(question=question, correctness_of_answer=True).first()
        
        # Получаем ответ пользователя из базы данных
        user_answer = TestAnswer.objects.filter(test_session=test_session, question=question).first()
        
        # Если ответ пользователя совпадает с правильным, увеличиваем балл
        if user_answer and user_answer.answer == correct_answer:
            total_points += 1

    context = {
        'test': test,
        'points': total_points,
        'max_points': max_points,
    }

    return render(request, 'test_passing/test_completion.html', context)



# Сохранение ответа на вопрос
@login_required
def submit_answer(request, session_id):
    # Получаем сессию теста
    test_session = get_object_or_404(TestSession, id=session_id, student=request.user.student)

    # Проверяем, не завершен ли тест
    if test_session.completed:
        return redirect('test_passing:test_completion', session_id=session_id)

    # Получаем данные из POST-запроса
    question_id = request.POST.get('question_id')
    answer_id = request.POST.get('answer')

    # Проверяем, что ответ существует
    question = get_object_or_404(Question, id=question_id, test=test_session.test)
    answer = get_object_or_404(Answer, id=answer_id, question=question)

    # Сохраняем ответ в базе данных
    TestAnswer.objects.update_or_create(
        test_session=test_session,
        question=question,
        defaults={'answer': answer}
    )

    # Получаем следующий вопрос
    next_question = Question.objects.filter(test=test_session.test, id__gt=question.id).first()

    if next_question:
        # Перенаправляем к следующему вопросу
        return redirect('test_passing:test_execution', session_id=test_session.id)

    # Если вопросов больше нет, завершить тест
    test_session.completed = True
    test_session.save()
    return redirect('test_passing:test_completion', session_id=test_session.id)



# Страница истечения времени теста
def test_expired(request):
    # Проверяем, что пользователь авторизован и является студентом
    if not request.user.is_authenticated or not hasattr(request.user, 'student'):
        return HttpResponseForbidden("Доступ запрещен.")

    # Проверяем, что сессия теста действительно истекла (возможно, сессия уже была завершена)
    # Например, можно проверить состояние сессии в базе данных, если сессия уже завершена, то мы можем отобразить страницу с ошибкой или окончанием
    test_session = TestSession.objects.filter(student=request.user.student, completed=False).first()
    if not test_session:
        return redirect('test_passing:test_list')

    # Отображаем страницу уведомления о том, что время теста истекло
    return render(request, 'test_passing/test_expired.html')




# Старт теста (страница с информацией перед началом теста)
@login_required
def test_start(request, test_id):
    # Проверяем, что пользователь авторизован и является студентом
    if not request.user.is_authenticated:
        return redirect('users:login')

    if not hasattr(request.user, 'student'):
        return HttpResponseForbidden("Только студенты могут проходить этот тест")

    # Проверяем существование теста
    test = Test.objects.filter(id=test_id).first()
    if not test:
        return HttpResponseForbidden("Тест не найден")

    context = {
        'test': test
    }

    # Отображаем страницу старта теста (начало теста)
    return render(request, 'test_passing/start_test.html', context)