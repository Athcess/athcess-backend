from django.db import models
from .chat import Chat

class Message(models.Model):
    message_id = models.CharField(primary_key=True, max_length=100)
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    content = models.TextField()
    sender_id = models.CharField(max_length=100)

    class Meta:
        db_table = "message"
    
    def __str__(self):
        return str(self.message_id)
