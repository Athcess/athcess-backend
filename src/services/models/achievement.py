from django.db import models

class Achievement(models.Model):
    achievement = models.CharField(primary_key=True, max_length=250)
    date = models.DateField()
    # user_id = models.ForeignKey(User, primary_key=True, max_length=100)

    class Meta:
        db_table = "achievement"
    
    def __str__(self):
        return str(self.achievement)