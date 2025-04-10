from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, QuestionForm, AnswerForm
from .models import Question, Answer
from django.http import Http404


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'questions': questions})


@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'post_question.html', {'form': form})


@login_required
def question_detail(request, id):
    # Separate query for the question and answers
    try:
        question = Question.objects.select_related('user').get(id=id)
    except Question.DoesNotExist:
        raise Http404("Question not found.")

    answers = Answer.objects.select_related('user').filter(question_id=id).order_by(
        '-created_at')

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', id=id)
    else:
        form = AnswerForm()
    return render(request, 'question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })


@login_required
def like_answer(request, answer_id):
    try:
        answer = Answer.objects.select_related('question').get(id=answer_id)
    except Answer.DoesNotExist:
        raise Http404("Answer not found.")

    if answer.likes.filter(id=request.user.id).exists():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)

    return redirect('question_detail', id=answer.question.id)
