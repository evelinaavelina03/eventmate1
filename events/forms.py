from django import forms
from .models import Event, EventChatMessage

class EventForm(forms.ModelForm):
    # Указываем, что для поля event_date мы будем использовать специальный HTML-виджет для ввода даты и времени
    event_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        label="Дата и время события"
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'interest', 'event_date', 'city', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'interest': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название события',
            'description': 'Описание',
            'interest': 'Категория интереса',
            'city': 'Город',
            'image': 'Фотография события',
        }

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = EventChatMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Напишите сообщение...'
            })
        }
        labels = {
            'message': '',
        }