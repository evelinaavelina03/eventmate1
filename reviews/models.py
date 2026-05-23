from django.db import models
from django.conf import settings
from events.models import Event
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reviewer', 'reviewed', 'event')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from django.db.models import Avg
        avg = Review.objects.filter(reviewed=self.reviewed).aggregate(Avg('rating'))['rating__avg']
        self.reviewed.rating_avg = avg if avg else 0
        self.reviewed.save(update_fields=['rating_avg'])