# core/views.py
from django.shortcuts import render
from django.db.models import Avg
from events.models import Event
from users.models import User, City
from reviews.models import Review
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
    
    # Статистика для главной страницы
    events_count = Event.objects.count()
    users_count = User.objects.count()
    cities_count = City.objects.count()
    
    # Средний рейтинг (если есть отзывы)
    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0
    
    return render(request, 'home.html', {
        'events': events,
        'events_count': events_count,
        'users_count': users_count,
        'cities_count': cities_count,
        'avg_rating': avg_rating,
    })