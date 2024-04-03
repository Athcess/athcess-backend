from django.db import models

class Verified(models.Model):
    verify_id = models.IntegerField(primary_key=True)
    status = models.BooleanField()
    TYPE_CHOICES = [
        ('pending', 'Pending'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    ]
    type = models.CharField(choices=TYPE_CHOICES)

    class Meta:
        db_table = "verified"

    def __str__(self):
        return f"Verified object {self.verify_id}"
