from django.db import models
from .blob_storage import BlobStorage as Blob
from .message import Message

class HaveAttachment(models.Model):
    Message_ID = models.ForeignKey(Message, on_delete=models.CASCADE)
    Object_ID = models.ForeignKey(Blob, on_delete=models.CASCADE)

    class Meta:
        db_table = "Have_Attachment"

    def __str__(self):
        return f"Attachment for Message {self.Message_ID}"
