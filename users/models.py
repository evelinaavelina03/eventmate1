from django.db import models
from django.contrib.auth.models import AbstractUser

class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Rating(models.Model):
    rating_id = models.SmallAutoField(primary_key=True)
    mark = models.SmallIntegerField()

    def __str__(self):
        return str(self.mark)

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, db_column='city_id')
    rating = models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True, blank=True, db_column='rating_id')
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class UserInterest(models.Model):
    user_interest_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    interest = models.ForeignKey('interests.Interest', on_delete=models.CASCADE, db_column='interest_id')

    class Meta:
        unique_together = ('user', 'interest')