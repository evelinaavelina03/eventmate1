from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from .models import Event, Status, StatusEvent, EventChatMessage
from .forms import EventForm, ChatMessageForm
from users.models import City, User
from interests.models import Interest
from reviews.models import Review
from ads.models import Response

def format_date_range(date_range_str):
    """Форматирует дату из формата YYYY-MM-DD в DD.MM.YYYY"""
    if not date_range_str:
        return ''
    if ' - ' in date_range_str:
        parts = date_range_str.split(' - ')
        if len(parts) == 2:
            start = parts[0].strip()
            end = parts[1].strip()
            if len(start) >= 10:
                start_f = f"{start[8:10]}.{start[5:7]}.{start[0:4]}"
            else:
                start_f = start
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
    
    search_query = request.GET.get('search', '')
    city_name = request.GET.get('city', '')
    interest_name = request.GET.get('interest', '')
    date_range = request.GET.get('date_range', '')
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if city_name:
        events = events.filter(city__name__icontains=city_name)
    
    if interest_name:
        events = events.filter(interest__name__icontains=interest_name)
    
    if date_range and ' - ' in date_range:
        dates = date_range.split(' - ')
        if len(dates) == 2:
            date_from = dates[0].strip()
            date_to = dates[1].strip()
            if date_from:
                events = events.filter(event_date__date__gte=date_from)
            if date_to:
                events = events.filter(event_date__date__lte=date_to)
    
    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    events_page = paginator.get_page(page_number)
    
    cities = City.objects.all()
    interests = Interest.objects.all()
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
    is_participant = False
    user_has_reviewed_author = False
    now = timezone.now()
    
    if event.event_date:
        is_past_event = event.event_date < now
    else:
        is_past_event = False
    
    is_not_author = False
    companions = []
    reviewed_companions_ids = []
    
    if request.user.is_authenticated:
        is_participant = event.requests.filter(user=request.user).exists()
        is_not_author = request.user != event.author
        user_has_reviewed_author = Review.objects.filter(
            reviewer=request.user,
            reviewed=event.author,
            event=event
        ).exists()
        
        # Находим напарников (принятые отклики)
        if is_past_event:
            companion_ids = Response.objects.filter(
                advertisement__event=event,
                status='accepted'
            ).filter(
                Q(user=request.user) | Q(advertisement__author=request.user)
            ).exclude(
                user=request.user
            ).values_list('user', flat=True).distinct()
            
            companions = User.objects.filter(pk__in=companion_ids)
            
            # Проверяем, на кого уже оставлены отзывы
            reviewed_companions_ids = Review.objects.filter(
                reviewer=request.user,
                reviewed__in=companions,
                event=event
            ).values_list('reviewed_id', flat=True)
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_participant': is_participant,
        'now': now,
        'is_past_event': is_past_event,
        'is_not_author': is_not_author,
        'user_has_reviewed_author': user_has_reviewed_author,
        'companions': companions,
        'reviewed_companions_ids': list(reviewed_companions_ids),
    })

# ========== ЧАТ ==========
@login_required
def event_chat(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.event = event
            msg.user = request.user
            msg.save()
            return redirect(f'/events/{event.id}/chat/')
    else:
        form = ChatMessageForm()
    
    messages_list = event.chat_messages.all()
    
    return render(request, 'events/event_chat.html', {
        'event': event,
        'messages': messages_list,
        'form': form,
    })

# ========== API ДЛЯ ЧАТА ==========
@login_required
def get_messages_api(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    last_id = request.GET.get('last_id', 0)
    messages = event.chat_messages.filter(id__gt=last_id).order_by('created_at')
    
    data = []
    for msg in messages:
        data.append({
            'id': msg.id,
            'username': msg.user.username,
            'message': msg.message,
            'created_at': msg.created_at.strftime('%d.%m.%Y %H:%M'),
            'is_mine': msg.user == request.user,
            'avatar': msg.user.avatar.url if msg.user.avatar else None,
        })
    
    return JsonResponse({'messages': data})

# ========== РЕДАКТИРОВАНИЕ СОБЫТИЯ ==========
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if event.author != request.user:
        messages.error(request, 'Вы можете редактировать только свои события')
        return redirect(f'/events/{event.id}/')
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Событие успешно обновлено!')
            return redirect(f'/events/{event.id}/')
    else:
        # Передаём текущую дату в правильном формате
        initial_data = {}
        if event.event_date:
            initial_data['event_date'] = event.event_date.strftime('%Y-%m-%dT%H:%M')
        form = EventForm(instance=event, initial=initial_data)
    
    return render(request, 'events/edit_event.html', {'form': form, 'event': event})


