from django.contrib import admin
from .models import Status, StatusEvent, Event

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(StatusEvent)
class StatusEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'city', 'interest', 'event_date', 'status', 'status_event', 'created_at')
    list_filter = ('status', 'status_event', 'city', 'interest')
    search_fields = ('title', 'description', 'author__username')
    raw_id_fields = ('author', 'city', 'interest')