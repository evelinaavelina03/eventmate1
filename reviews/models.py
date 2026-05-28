from django.db import models
from django.conf import settings
from events.models import Event
from django.core.validators import MinValueValidator, MaxValueValidator

User = settings.AUTH_USER_MODEL

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'reviewed', 'event')  # один отзыв на событие

    def __str__(self):
        return f"{self.reviewer} -> {self.reviewed}: {self.rating}"