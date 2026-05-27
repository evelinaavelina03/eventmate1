from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

from events.views import event_list, event_detail, create_event
from ads.views import listing_list, create_listing, listing_detail, create_response, manage_responses, update_response_status
from users.views import register, set_interests, profile, edit_profile
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('register/', register, name='register'),
    path('set-interests/', set_interests, name='set_interests'),
    
    # Страницы событий
    path('events/', event_list, name='events'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),
    path('events/create/', create_event, name='create_event'),
    
    # Страницы объявлений
    path('listings/', listing_list, name='listings'),
    path('listings/create/', create_listing, name='create_listing'),
    path('listings/<int:pk>/', listing_detail, name='listing_detail'),
    
    # Отклики на объявления
    path('listings/<int:pk>/respond/', create_response, name='create_response'),
    path('listings/<int:pk>/responses/', manage_responses, name='manage_responses'),
    path('responses/<int:pk>/<str:status>/', update_response_status, name='update_response_status'),
    
    # Аутентификация
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    
    # Профиль (важен порядок: сначала edit, потом profile с параметром)
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/', profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)