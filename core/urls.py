from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView   # <-- добавьте эту строку
from events.views import event_list, event_detail
from ads.views import listing_list, create_listing     # импортируем представления для объявлений

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    # Страницы событий
    path('events/', event_list, name='events'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),
    # Страницы объявлений
    path('listings/', listing_list, name='listings'),
    path('listings/create/', create_listing, name='create_listing'),
    path('login/', LoginView.as_view(template_name='home.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]