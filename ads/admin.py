from django.contrib import admin
from .models import Request

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'event__title')