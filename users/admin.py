from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import City, Rating, User, UserInterest

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('city_id', 'name')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('rating_id', 'mark')

class CustomUserAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'email', 'phone', 'city', 'rating', 'created_at')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('phone', 'birth_date', 'city', 'rating')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительно', {'fields': ('phone', 'birth_date', 'city', 'rating')}),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ('user_interest_id', 'user', 'interest')