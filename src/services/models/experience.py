from django.db import models
from users.models.custom_user import CustomUser


class Experience(models.Model):
    experience_id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=150)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    username = models.ForeignKey(CustomUser, max_length=100, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        db_table = "experience"
        indexes = [
            models.Index(fields=['experience_id', 'username']),
        ]
    
    def __str__(self):
        return str(self.topic)