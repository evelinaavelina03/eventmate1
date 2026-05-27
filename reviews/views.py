
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event
from users.models import User
from .forms import ReviewForm
from .models import Review

@login_required
def create_review(request, event_id, user_id):
    event = get_object_or_404(Event, id=event_id)
    reviewed = get_object_or_404(User, id=user_id)
    
    # Проверка: участвовал ли пользователь в событии
    if not event.requests.filter(user=request.user).exists():
        messages.error(request, 'Вы не участвовали в этом событии')
        return redirect('event_detail', event_id=event.id)
    
    # Проверка: не оставлял ли уже отзыв
    if Review.objects.filter(reviewer=request.user, reviewed=reviewed, event=event).exists():
        messages.warning(request, 'Вы уже оставляли отзыв на этого пользователя')
        return redirect('event_detail', event_id=event.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed = reviewed
            review.event = event
            review.save()
            messages.success(request, f'Отзыв о {reviewed.username} оставлен! Спасибо!')
            return redirect('profile', username=reviewed.username)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/create_review.html', {
        'form': form,
        'reviewed': reviewed,
        'event': event,
    })
