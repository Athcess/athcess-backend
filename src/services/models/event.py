from django.contrib.postgres.fields import ArrayField
from django.db import models

class Event(models.Model):
    Event_ID = models.AutoField(primary_key=True)
    #Org_Name = models.ForeignKey('Organization', on_delete=models.CASCADE)
    Content = models.CharField(max_length=200)
    Time_Post = models.DateTimeField()
    Like = ArrayField(models.IntegerField(), default=list)

    class Meta:
        db_table = "event"

    def __str__(self):
        return f"Event ID: {self.Event_ID}"
