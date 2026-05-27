from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Advertisement, Response
from .forms import AdvertisementForm, ResponseForm
from events.models import Event

def listing_list(request):
    """Список всех активных объявлений"""
    listings = Advertisement.objects.filter(status='active').order_by('-created_at')
    return render(request, 'ads/listing_list.html', {'listings': listings})

def listing_detail(request, pk):
    listing = get_object_or_404(Advertisement, pk=pk)
    has_responded = False
    if request.user.is_authenticated:
        # Проверяем, есть ли уже отклик от этого пользователя на это объявление
        has_responded = Response.objects.filter(advertisement=listing, user=request.user).exists()
    return render(request, 'ads/listing_detail.html', {
        'listing': listing,
        'has_responded': has_responded,
    })

@login_required
def create_listing(request):
    """Создание нового объявления"""
    # Если передан параметр event, предзаполняем поле
    event_id = request.GET.get('event')
    initial = {}
    if event_id:
        event = get_object_or_404(Event, pk=event_id)
        initial['event'] = event

    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.save()
            messages.success(request, 'Объявление успешно создано!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = AdvertisementForm(initial=initial)
    return render(request, 'ads/create_listing.html', {'form': form})

@login_required
def create_response(request, pk):
    """Создание отклика на объявление"""
    advertisement = get_object_or_404(Advertisement, pk=pk)
    
    # Нельзя откликаться на своё объявление
    if advertisement.author == request.user:
        messages.error(request, 'Вы не можете откликаться на своё объявление.')
        return redirect('listing_detail', pk=pk)
    
    # Проверяем, не откликался ли уже пользователь
    if Response.objects.filter(advertisement=advertisement, user=request.user).exists():
        messages.error(request, 'Вы уже откликались на это объявление.')
        return redirect('listing_detail', pk=pk)
    
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.advertisement = advertisement
            response.user = request.user
            response.save()
            messages.success(request, 'Ваш отклик отправлен автору объявления!')
            return redirect('listing_detail', pk=pk)
    else:
        form = ResponseForm()
    
    return render(request, 'ads/create_response.html', {
        'form': form,
        'advertisement': advertisement,
    })

@login_required
def manage_responses(request, pk):
    """Управление откликами на своё объявление (только для автора)"""
    advertisement = get_object_or_404(Advertisement, pk=pk)
    
    # Проверяем, что текущий пользователь — автор
    if advertisement.author != request.user:
        messages.error(request, 'Вы не можете управлять откликами на чужое объявление.')
        return redirect('listing_detail', pk=pk)
    
    responses = advertisement.responses.all().order_by('-created_at')
    return render(request, 'ads/manage_responses.html', {
        'advertisement': advertisement,
        'responses': responses,
    })

@login_required
def update_response_status(request, pk, status):
    """Обновление статуса отклика (принять/отклонить)"""
    response = get_object_or_404(Response, pk=pk)
    advertisement = response.advertisement
    
    # Только автор объявления может менять статус
    if advertisement.author != request.user:
        messages.error(request, 'У вас нет прав для этого действия.')
        return redirect('listing_detail', pk=advertisement.pk)
    
    if status not in ['accepted', 'rejected']:
        messages.error(request, 'Некорректный статус.')
        return redirect('manage_responses', pk=advertisement.pk)
    
    response.status = status
    response.save()
    
    # Если статус "accepted", можно закрыть объявление (опционально)
    if status == 'accepted':
        advertisement.status = 'closed'
        advertisement.save()
        messages.success(request, f'Вы приняли отклик от {response.user.username}. Объявление закрыто.')
    else:
        messages.success(request, f'Вы отклонили отклик от {response.user.username}.')
    
    return redirect('manage_responses', pk=advertisement.pk)