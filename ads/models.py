from django.db import models

class Request(models.Model):
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='requests')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='requests')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Request from {self.user.username} for {self.event.title}"