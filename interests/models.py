from django.db import models

class Type(models.Model):
    name_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name_type

class Interest(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserInterest(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'interest')
    
    def __str__(self):
        return f"{self.user.username} - {self.interest.name}"