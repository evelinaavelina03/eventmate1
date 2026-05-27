from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:event_id>/<int:user_id>/', views.create_review, name='create_review'),
]