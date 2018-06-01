from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import timezone

from .models import Category, Thread, Answer

def index(request):
    category_list = Category.objects.all()
    context = {'category_list': category_list}
    return render(request, 'forum/index.html', context)

def category_view(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    context = {'category': category}
    return render(request, 'forum/category.html', context)

def thread_view(reqest, category_id, thread_id):
    try:
        thread = Thread.objects.get(pk = thread_id)
        category = Category.objects.get(pk = category_id)
    except Thread.DoesNotExist:
        raise Http404("Thread doesn not exist")
    answer_list = thread.answer_set.order_by('answer_date')
    context = {'answer_list': answer_list, 'thread': thread, 'category': category}
    return render(reqest, 'forum/thread.html', context)

def not_logged(request):
    return render(request, 'forum/not_logged.html')

def create_thread(request, category_id):
    if not request.user.is_authenticated:
        return redirect('forum:not_logged')
    user = request.user.username
    time = timezone.now()
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    thread_text = request.POST['thread_text']
    answer_text = request.POST['answer_text']

    thread = Thread(
        thread_text  = thread_text, 
        thread_date = time, 
        thread_author = user,
        category = category
        )
    thread.save()
    answer = Answer(
        answer_text = answer_text,
        answer_date = time,
        answer_author = user,
        thread = thread
        )
    answer.save()

    return redirect('forum:category_view', category_id=category_id)

def create_answer(request, category_id, thread_id):
    if not request.user.is_authenticated:
        return redirect('forum:not_logged')
    user = request.user.username
    time = timezone.now()
    try:
        thread = Thread.objects.get(pk=thread_id)
    except Category.DoesNotExist:
        raise Http404("Thread does not exist")
    answer_text = request.POST['answer_text']
    answer = Answer(
        answer_text = answer_text,
        answer_date = time,
        answer_author = user,
        thread = thread
        )
    answer.save()

    return redirect('forum:thread_view', category_id=category_id, thread_id=thread_id)