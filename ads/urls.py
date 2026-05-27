from django.urls import path
from . import views

app_name = 'ads'

urlpatterns = [
    path('event/<int:event_id>/request/', views.create_request, name='create_request'),
]