from django.db import models
from .chat import Chat
from users.models.custom_user import CustomUser

class Owns(models.Model):
    username = models.OneToOneField(CustomUser, unique=True, on_delete=models.CASCADE)
    chat_id = models.OneToOneField(Chat, primary_key=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'owns'

    def __str__(self):
        return str(self.chat_id, self.username) #also want to return self.user_id

