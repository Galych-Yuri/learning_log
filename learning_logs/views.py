from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryFofm


# Create your views here.
def index(request):
    """Повертає головну сторінку журналу спостережень."""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Відображає всі теми."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # Пересвідчитися, що тема належить поточному користувачеві.
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """
    Функція реагує на перші запити зі сторінки new_topic.\n
    Опрацьовує дані що надходять з надісланої форми.\n
    Переадресовує користувача до сторінки з темами.
    :param request:
    :return: redirect to learning_logs:topics
    """
    if request.method != 'POST':
        # Жодних даних не відправлено, створити порожню форму
        form = TopicForm()
    else:
        # Відправлений ПОСТ. Обробити дані
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Показати порожню або недійну форму
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # Жодних даних не надіслано; створити порожню фотму.
        form = EntryFofm()
    else:
        # Отримані дані у POST- запиті; обробити дані
        form = EntryFofm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Показати порожню фбо недійсну форму.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # Пересвідчитися, що тема належить поточному користувачеві.
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryFofm(instance=entry)
    else:
        # POST data submited; process data
        form = EntryFofm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
