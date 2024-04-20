from django.db import models
from users.models.custom_user import CustomUser


class IsFriendOf(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_id')
    friend_username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friend_user_id')
    status = models.CharField(max_length=50, choices=[('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected')])
    since = models.DateTimeField(blank=True, null=True)


    class Meta:
        db_table = "is_friend_of"
    
    def __str__(self):
        return str(self.id)
