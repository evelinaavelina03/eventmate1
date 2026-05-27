from django.db import models
from users.models import User
from events.models import Event

class Advertisement(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('closed', 'Закрыто'),
        ('cancelled', 'Отменено'),
    ]
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='advertisements', verbose_name="Событие")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisements', verbose_name="Автор")
    companions_needed = models.PositiveIntegerField(default=1, verbose_name="Нужно напарников")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Request(models.Model):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='requests')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='requests')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Request from {self.user.username} for {self.event.title}"
    
class Response(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонён'),
        ('cancelled', 'Отменён'),
    ]
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='responses')
    message = models.TextField(verbose_name="Сообщение автору", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('advertisement', 'user')  # один пользователь может откликнуться только один раз

    def __str__(self):
        return f"{self.user.username} -> {self.advertisement.title}"