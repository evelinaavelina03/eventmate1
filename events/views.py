from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Event, Status, StatusEvent
from .forms import EventForm

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            # Используем get_or_create с фильтром по имени, но если есть дубли, то нужно либо удалить дубли, либо использовать first()
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
    all_events = Event.objects.all().order_by('event_date')
    paginator = Paginator(all_events, 6)  # 6 событий на страницу
    page_number = request.GET.get('page')
    events = paginator.get_page(page_number)
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/event_detail.html', {'event': event})