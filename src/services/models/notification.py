from django.db import models
from users.models.custom_user import CustomUser



class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    
    TYPE_CHOICES = [
        ('post', 'Post'),
        ('friend_request', 'Friend Request'),
    ]
    type = models.CharField(choices=TYPE_CHOICES)

    class Meta:
        db_table = "notification"

    def __str__(self):
        return f"Notification ID: {self.Noti_ID}"
