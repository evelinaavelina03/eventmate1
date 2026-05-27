from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event
from .models import Request

def listing_list(request):
    return render(request, 'ads/listing_list.html', {'listings': []})

@login_required
def create_listing(request):
    return render(request, 'ads/create_listing.html', {'form': None})

@login_required
def create_request(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if not Request.objects.filter(event=event, user=request.user).exists():
        Request.objects.create(event=event, user=request.user)
        messages.success(request, f'✅ Вы откликнулись на событие "{event.title}"!')
    else:
        messages.warning(request, f'⚠️ Вы уже откликались на событие "{event.title}".')
    
    # Прямой URL (работает всегда)
    return redirect(f'/events/{event_id}/')