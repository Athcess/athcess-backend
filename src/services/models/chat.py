from django.db import models
from django.contrib.postgres.fields import ArrayField


class Chat(models.Model):
    chat_id = models.CharField(max_length=100)
    chat_name = models.CharField(max_length=100)
    members = ArrayField(models.CharField(max_length=100))

    class Meta:
        db_table = "chat"

    def __unicode__(self):
        return str(self.chat_id)