from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Event, Status, StatusEvent
from .forms import EventForm
from users.models import City
from interests.models import Interest

def format_date_range(date_range_str):
    """Форматирует дату из формата YYYY-MM-DD в DD.MM.YYYY"""
    if not date_range_str:
        return ''
    if ' - ' in date_range_str:
        parts = date_range_str.split(' - ')
        if len(parts) == 2:
            start = parts[0].strip()
            end = parts[1].strip()
            # Форматируем start (2026-05-18 → 18.05.2026)
            if len(start) >= 10:
                start_f = f"{start[8:10]}.{start[5:7]}.{start[0:4]}"
            else:
                start_f = start
            # Форматируем end (2026-06-03 → 03.06.2026)
            if len(end) >= 10:
                end_f = f"{end[8:10]}.{end[5:7]}.{end[0:4]}"
            else:
                end_f = end
            return f"{start_f} - {end_f}"
    else:
        if len(date_range_str) >= 10:
            return f"{date_range_str[8:10]}.{date_range_str[5:7]}.{date_range_str[0:4]}"
    return date_range_str

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            status = Status.objects.filter(name='active').first()
            if not status:
                status = Status.objects.create(name='active')
            event.status = status
            status_event = StatusEvent.objects.filter(name='in_process').first()
            if not status_event:
                status_event = StatusEvent.objects.create(name='in_process')
            event.status_event = status_event
            event.save()
            return redirect(f'/events/{event.pk}/')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

def event_list(request):
    events = Event.objects.all().order_by('event_date')
    
    # Получаем параметры фильтрации
    search_query = request.GET.get('search', '')
    city_name = request.GET.get('city', '')
    interest_name = request.GET.get('interest', '')
    date_range = request.GET.get('date_range', '')
    
    # Фильтр по поиску
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Фильтр по городу
    if city_name:
        events = events.filter(city__name__icontains=city_name)
    
    # Фильтр по категории
    if interest_name:
        events = events.filter(interest__name__icontains=interest_name)
    
    # Фильтр по диапазону дат
    if date_range and ' - ' in date_range:
        dates = date_range.split(' - ')
        if len(dates) == 2:
            date_from = dates[0].strip()
            date_to = dates[1].strip()
            if date_from:
                events = events.filter(event_date__date__gte=date_from)
            if date_to:
                events = events.filter(event_date__date__lte=date_to)
    
    # Пагинация
    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    events_page = paginator.get_page(page_number)
    
    # Данные для фильтров
    cities = City.objects.all()
    interests = Interest.objects.all()
    
    # Форматируем дату для отображения
    date_range_formatted = format_date_range(date_range)
    
    return render(request, 'events/event_list.html', {
        'events': events_page,
        'cities': cities,
        'interests': interests,
        'search_query': search_query,
        'city_name': city_name,
        'selected_interest_name': interest_name,
        'date_range': date_range,
        'date_range_formatted': date_range_formatted,
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})