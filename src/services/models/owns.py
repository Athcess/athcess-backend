# Not done, Need to import user_id 
from django.db import models
from .chat import Chat

class Owns(models.Model):
    # user_id = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
    chat_id = models.ForeignKey(Chat, primary_key=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'owns'

    def __str__(self):
        return str(self.chat_id) #also want to return self.user_id

