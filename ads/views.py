from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def listing_list(request):
    return render(request, 'ads/listing_list.html', {'listings': []})

@login_required
def create_listing(request):
    # Пока просто показываем форму-заглушку
    return render(request, 'ads/create_listing.html', {'form': None})