from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import ReviewForm
from .models import Review
from events.models import Event
from users.models import User

@login_required
def create_review(request, event_id, user_id):
    event = get_object_or_404(Event, pk=event_id)
    reviewed_user = get_object_or_404(User, pk=user_id)
    
    # Проверка: событие должно быть завершено
    if event.event_date > timezone.now():
        messages.error(request, 'Отзыв можно оставить только после завершения события.')
        return redirect(f'/events/{event_id}/')
    
    # Проверка: нельзя оставить отзыв самому себе
    if request.user == reviewed_user:
        messages.error(request, 'Вы не можете оставить отзыв самому себе.')
        return redirect(f'/events/{event_id}/')
    
    # Проверка: не оставлял ли уже отзыв
    if Review.objects.filter(reviewer=request.user, reviewed=reviewed_user, event=event).exists():
        messages.error(request, 'Вы уже оставляли отзыв этому пользователю на данное событие.')
        return redirect(f'/events/{event_id}/')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed = reviewed_user
            review.event = event
            review.save()
            reviewed_user.update_rating()
            messages.success(request, f'Спасибо за ваш отзыв о пользователе {reviewed_user.username}!')
            return redirect(f'/events/{event_id}/')
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/create_review.html', {
        'form': form,
        'event': event,
        'reviewed_user': reviewed_user,
    })