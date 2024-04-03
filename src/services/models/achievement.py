from django.db import models
from users.models.custom_user import CustomUser

class Achievement(models.Model):
    achievement = models.CharField(unique=True, max_length=250)
    date = models.DateField(primary_key=True)
    username = models.OneToOneField(CustomUser, max_length=100, on_delete=models.CASCADE)

    class Meta:
        db_table = "achievement"
    
    def __str__(self):
        return str(self.achievement, self.username)