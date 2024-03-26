from django.db import models

class HaveAttachment(models.Model):
    #Message_ID = models.ForeignKey('Message', on_delete=models.CASCADE)
    #Object_ID = models.ForeignKey('Object', on_delete=models.CASCADE)

    class Meta:
        db_table = "Have_Attachment"

    def __str__(self):
        return f"Attachment for Message {self.Message_ID}"
