
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(1, '⭐ 1'), (2, '⭐⭐ 2'), (3, '⭐⭐⭐ 3'), (4, '⭐⭐⭐⭐ 4'), (5, '⭐⭐⭐⭐⭐ 5')]),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Поделитесь впечатлениями...'}),
        }
        labels = {
            'rating': 'Оценка',
            'comment': 'Комментарий (необязательно)',
        }
