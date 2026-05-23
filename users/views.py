from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from interests.models import Interest
from .models import User, UserInterest
from events.models import Event
from .forms import UserEditForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    events = Event.objects.filter(author=user).order_by('-created_at')
    # Пока без объявлений, добавим позже
    listings = []
    return render(request, 'users/profile.html', {
        'profile_user': user,
        'events': events,
        'listings': listings,
    })

@login_required
def set_interests(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('interests')
        UserInterest.objects.filter(user=request.user).delete()
        for interest_id in selected_ids:
            UserInterest.objects.create(user=request.user, interest_id=interest_id)
        return redirect('home')
    else:
        interests = Interest.objects.all()
        return render(request, 'users/set_interests.html', {'interests': interests})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('set_interests')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})