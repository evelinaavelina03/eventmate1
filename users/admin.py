from django.contrib import admin
from .models import City, User, Author, Rating

admin.site.register(City)
admin.site.register(User)
admin.site.register(Author)
admin.site.register(Rating)