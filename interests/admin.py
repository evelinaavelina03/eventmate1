from django.contrib import admin
from .models import Type, Interest

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'name_type')

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('interest_id', 'name', 'type', 'icon')