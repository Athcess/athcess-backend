from django.contrib.postgres.fields import ArrayField
from django.db import models
from users.models.custom_user import Organization


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    club = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1000)
    has_attachment = models.BooleanField(default=False)
    like = models.TextField(default='', blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        db_table = "event"
        indexes = [
            models.Index(fields=['event_id', 'club']),
        ]

    def __str__(self):
        return f"Event ID: {self.event_id}"
