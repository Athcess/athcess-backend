from django.db import models
from users.models.custom_user import CustomUser


class Experience(models.Model):
    topic = models.CharField(primary_key=True, max_length=150)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    create_at = models.DateField()
    username = models.ForeignKey(CustomUser, max_length=100, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        db_table = "experience"
    
    def __str__(self):
        return str(self.topic)