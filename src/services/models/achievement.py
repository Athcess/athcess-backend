from django.db import models
from users.models.custom_user import CustomUser


class Achievement(models.Model):
    topic = models.TextField(unique=True, max_length=250)
    sub_topic = models.TextField(max_length=250)
    description = models.TextField(max_length=1000)
    create_at = models.DateField(primary_key=True)
    date = models.DateField(blank=True, null=True)
    username = models.ForeignKey(CustomUser, max_length=100, on_delete=models.CASCADE)

    class Meta:
        db_table = "achievement"
    
    def __str__(self):
        return str(self.achievement, self.username)