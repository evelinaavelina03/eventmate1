from django.db import models

class Status(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('closed', 'Закрыто'),
        ('moderation', 'На модерации'),
    ]
    name = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.get_name_display()

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title