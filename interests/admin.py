from django.contrib import admin
from .models import Type, Interest, UserInterest

admin.site.register(Type)
admin.site.register(Interest)
admin.site.register(UserInterest)