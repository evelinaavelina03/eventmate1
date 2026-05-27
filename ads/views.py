from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Advertisement, Response
from .forms import AdvertisementForm, ResponseForm, AdvertisementEditForm
from events.models import Event
from .models import Notification

def listing_list(request):
    listings = Advertisement.objects.filter(status='active').order_by('-created_at')
    return render(request, 'ads/listing_list.html', {'listings': listings})

def listing_detail(request, pk):
    listing = get_object_or_404(Advertisement, pk=pk)
    has_responded = False
    if request.user.is_authenticated:
        has_responded = Response.objects.filter(advertisement=listing, user=request.user).exists()
    return render(request, 'ads/listing_detail.html', {
        'listing': listing,
        'has_responded': has_responded,
    })

@login_required
def create_listing(request):
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
def edit_listing(request, pk):
    listing = get_object_or_404(Advertisement, pk=pk)
    
    if listing.author != request.user:
        messages.error(request, 'Вы можете редактировать только свои объявления.')
        return redirect('listing_detail', pk=pk)
    
    if request.method == 'POST':
        form = AdvertisementEditForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление успешно обновлено!')
            return redirect('listing_detail', pk=pk)
    else:
        form = AdvertisementEditForm(instance=listing)
    
    return render(request, 'ads/edit_listing.html', {'form': form, 'listing': listing})

@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Advertisement, pk=pk)
    
    if listing.author != request.user:
        messages.error(request, 'Вы можете удалять только свои объявления.')
        return redirect('listing_detail', pk=pk)
    
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Объявление успешно удалено.')
        return redirect('listings')
    
    return render(request, 'ads/confirm_delete.html', {'listing': listing})


@login_required
def create_response(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    
    if advertisement.author == request.user:
        messages.error(request, 'Вы не можете откликаться на своё объявление.')
        return redirect('listing_detail', pk=pk)
    
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
            
            # 🔔 СОЗДАЁМ УВЕДОМЛЕНИЕ ДЛЯ АВТОРА ОБЪЯВЛЕНИЯ
            Notification.objects.create(
                recipient=advertisement.author,
                sender=request.user,
                notification_type='response',
                advertisement=advertisement,
                message=f'{request.user.username} откликнулся(ась) на ваше объявление "{advertisement.title}".'
            )
            
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
    advertisement = get_object_or_404(Advertisement, pk=pk)
    
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
    response = get_object_or_404(Response, pk=pk)
    advertisement = response.advertisement
    
    if advertisement.author != request.user:
        messages.error(request, 'У вас нет прав для этого действия.')
        return redirect('listing_detail', pk=advertisement.pk)
    
    if status not in ['accepted', 'rejected']:
        messages.error(request, 'Некорректный статус.')
        return redirect('manage_responses', pk=advertisement.pk)
    
    response.status = status
    response.save()
    
    # 🔔 СОЗДАЁМ УВЕДОМЛЕНИЕ ДЛЯ ТОГО, КТО ОТКЛИКНУЛСЯ
    if status == 'accepted':
        advertisement.status = 'closed'
        advertisement.save()
        Notification.objects.create(
            recipient=response.user,
            sender=request.user,
            notification_type='response_accepted',
            advertisement=advertisement,
            message=f'Автор объявления "{advertisement.title}" принял(а) ваш отклик.'
        )
        messages.success(request, f'Вы приняли отклик от {response.user.username}. Объявление закрыто.')
    else:
        Notification.objects.create(
            recipient=response.user,
            sender=request.user,
            notification_type='response_rejected',
            advertisement=advertisement,
            message=f'Автор объявления "{advertisement.title}" отклонил(а) ваш отклик.'
        )
        messages.success(request, f'Вы отклонили отклик от {response.user.username}.')
    
    return redirect('manage_responses', pk=advertisement.pk)

@login_required
def notifications(request):
    notifications = request.user.notifications.all()
    return render(request, 'ads/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')