from django.db import models

class City(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Author: {self.user.username}"

class Rating(models.Model):
    MARK_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.IntegerField(choices=MARK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.mark}"