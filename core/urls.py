from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

from ads.views import listing_list, create_listing, listing_detail, create_response, manage_responses, update_response_status
from users.views import register, set_interests, profile, edit_profile
from core.views import home
from ads.views import edit_listing, delete_listing
from ads.views import notifications, mark_notification_read

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('register/', register, name='register'),
    path('set-interests/', set_interests, name='set_interests'),
    
    # Страницы событий
    path('events/', include('events.urls')),
    
    # Страницы объявлений
    path('listings/', listing_list, name='listings'),
    path('listings/create/', create_listing, name='create_listing'),
    path('listings/<int:pk>/', listing_detail, name='listing_detail'),
    path('listings/<int:pk>/edit/', edit_listing, name='edit_listing'),
    path('listings/<int:pk>/delete/', delete_listing, name='delete_listing'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/<int:pk>/read/', mark_notification_read, name='mark_notification_read'),
    
    # Отклики на объявления
    path('listings/<int:pk>/respond/', create_response, name='create_response'),
    path('listings/<int:pk>/responses/', manage_responses, name='manage_responses'),
    path('responses/<int:pk>/<str:status>/', update_response_status, name='update_response_status'),
    
    # Аутентификация
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    
    # Профиль
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/', profile, name='profile'),
    
    # Отзывы
    path('reviews/', include('reviews.urls')),  # ← ДОБАВИТЬ ЭТУ СТРОКУ    
    # Добавляем маршруты для ads
    path('ads/', include('ads.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)