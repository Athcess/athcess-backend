from django.db import models

class Experience(models.Model):
    topic = models.CharField(primary_key=True, max_length=150)
    date = models.DateField()
    # user_id = models.ForeignKey(User, primary_key=True, max_length=100)
    description = models.TextField()

    class Meta:
        db_table = "experience"
    
    def __str__(self):
        return str(self.topic)