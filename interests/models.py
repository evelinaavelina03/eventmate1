from django.db import models

class Type(models.Model):
    type_id = models.AutoField(primary_key=True)
    name_type = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_type

class Interest(models.Model):
    interest_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(Type, on_delete=models.PROTECT, db_column='type_id')
    icon = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'type')

    def __str__(self):
        return f"{self.name} ({self.type.name_type})"