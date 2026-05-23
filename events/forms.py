from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    # Указываем, что для поля event_date мы будем использовать специальный HTML-виджет для ввода даты и времени
    event_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        label="Дата и время события"
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'interest', 'event_date', 'city', 'image'] # image - это наше новое поле
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'interest': forms.Select(),
            'city': forms.Select(),
        }
        labels = {
            'title': 'Название события',
            'description': 'Описание',
            'interest': 'Категория интереса',
            'city': 'Город',
            'image': 'Фотография события',
        }