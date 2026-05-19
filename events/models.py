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

class StatusEvent(models.Model):
    STATUS_EVENT_CHOICES = [
        ('done', 'Завершено'),
        ('not_done', 'Не завершено'),
        ('in_process', 'В процессе'),
    ]
    name = models.CharField(max_length=20, choices=STATUS_EVENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.get_name_display()

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Связи
    interest = models.ForeignKey('interests.Interest', on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    city = models.ForeignKey('users.City', on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='events')
    status_event = models.ForeignKey(StatusEvent, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Дополнительные поля
    event_date = models.DateTimeField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    
    # Статус модерации
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title