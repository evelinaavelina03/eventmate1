from django.db import models

class Request(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    advertisement = models.ForeignKey('events.Event', on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'advertisement')
    
    def __str__(self):
        return f"Отклик от {self.user.username} на {self.advertisement.title}"