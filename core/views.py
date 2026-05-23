# core/views.py
from django.shortcuts import render
from events.models import Event
from django.utils import timezone

def home(request):
    if request.user.is_authenticated:
        # Получаем ID интересов текущего пользователя
        user_interests = request.user.userinterest_set.values_list('interest_id', flat=True)
        events = Event.objects.filter(
            interest_id__in=user_interests,
            event_date__gte=timezone.now()
        ).order_by('event_date')[:10]
    else:
        # Для неавторизованных — все предстоящие события
        events = Event.objects.filter(event_date__gte=timezone.now()).order_by('event_date')[:10]
    return render(request, 'home.html', {'events': events})