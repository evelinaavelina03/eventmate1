from django.db import models
import os

# Функция для формирования пути к файлу должна быть вне класса, чтобы не было ошибок с self
def event_photo_path(instance, filename):
    # Получаем расширение файла
    ext = filename.split('.')[-1]
    # Формируем новое имя файла (используем pk, если он уже есть, иначе временно None)
    if instance.pk:
        new_filename = f"event_{instance.pk}.{ext}"
        return os.path.join('event_photos', f'event_{instance.pk}', new_filename)
    else:
        # Если объект ещё не сохранён, кладём во временную папку
        return os.path.join('event_photos', 'temp', filename)

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
    
    # Поле для изображения (новое, вместо image_url)
    image = models.ImageField(upload_to=event_photo_path, blank=True, null=True, verbose_name="Изображение события")
    
    # Статус модерации
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_participants_count(self):
        """Возвращает количество участников (откликов) на событие"""
        return self.requests.count()
    
    def get_participants(self):
        """Возвращает список участников события"""
        return [request.user for request in self.requests.all()]