from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

from events.views import event_list, event_detail, create_event   # исправлено
from ads.views import listing_list, create_listing
from users.views import register, set_interests
from core.views import home
from users.views import register, set_interests, profile, edit_profile # добавлен profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('register/', register, name='register'),
    path('set-interests/', set_interests, name='set_interests'),
    
    # Страницы событий
    path('events/', event_list, name='events'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),
    path('events/create/', create_event, name='create_event'),   # один раз
    
    # Страницы объявлений
    path('listings/', listing_list, name='listings'),
    path('listings/create/', create_listing, name='create_listing'),
    
    # Аутентификация
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    #профиль
    path('profile/<str:username>/', profile, name='profile'),
    path('profile/', profile, name='my_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]

# Для разработки: обслуживание загруженных пользователями файлов (медиа)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)