from django.db import models

class Verified(models.Model):
    Verified_ID = models.IntegerField(primary_key=True)
    Status = models.BooleanField()
    TYPE_CHOICES = [
        ('type1', 'Type 1'),
        ('type2', 'Type 2'),
        ('type3', 'Type 3'),
    ]
    Type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    class Meta:
        db_table = "Verified"

    def __str__(self):
        return f"Verified object {self.Verified_ID}"
