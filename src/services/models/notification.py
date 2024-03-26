from django.db import models

class Notification(models.Model):
    Noti_ID = models.AutoField(primary_key=True)
    #User_ID = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    
    TYPE_CHOICES = [
        ('type1', 'Type 1'),
        ('type2', 'Type 2'),
        ('type3', 'Type 3'),
    ]
    Type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    class Meta:
        db_table = "notification"

    def __str__(self):
        return f"Notification ID: {self.Noti_ID}"
