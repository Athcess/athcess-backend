from django.contrib.postgres.fields import ArrayField
from django.db import models
from users.models.custom_user import Organization

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    club = models.ForeignKey(Organization, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    like = ArrayField(models.IntegerField(), default=list)

    class Meta:
        db_table = "event"

    def __str__(self):
        return f"Event ID: {self.event_id}"
