"""
Додавання нових тем. Форма, що дозволяє користувачу
вводити та відправляти інформацію
"""
from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    """
    Найпростіша версія ModelForm містить вкладений клас Мета що описує
    на якій моделі слід базувати форму та які поля до неї додавати.
    """

    class Meta:
        model = Topic
        fields = ['text']
        label = {'text': ''}


class EntryFofm(forms.ModelForm):
    """"""

    class Meta:
        model = Entry
        fields = ['text']
        label = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
