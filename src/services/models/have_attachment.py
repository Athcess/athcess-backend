from django.db import models
from .blob_storage import BlobStorage
from .message import Message

class HaveAttachment(models.Model):
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE)
    attachment = models.ForeignKey(BlobStorage, on_delete=models.CASCADE)

    class Meta:
        db_table = "have_attachment"

    def __str__(self):
        return f"Attachment for Message {self.message_id}, {self.attachment}"
