from django import forms
from .models import Advertisement
from .models import Response

class AdvertisementEditForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'companions_needed', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'companions_needed': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Напишите пару слов о себе...'}),
        }
        labels = {
            'message': 'Сообщение автору',
        }
class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'event', 'companions_needed']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-select'}),
            'companions_needed': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'title': 'Заголовок объявления',
            'description': 'Кого ищем, условия',
            'event': 'Мероприятие',
            'companions_needed': 'Сколько человек нужно',
        }