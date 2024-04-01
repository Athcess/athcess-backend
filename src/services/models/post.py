from django.contrib.postgres.fields import ArrayField
from django.db import models

class Post(models.Model):
    Post_ID = models.AutoField(primary_key=True)
    #User_ID = models.ForeignKey('User', on_delete=models.CASCADE)
    Date_Post = models.DateField()
    Time_Post = models.TimeField()
    Description = models.CharField(max_length=200)
    Like = ArrayField(models.IntegerField(), default=list)

    class Meta:
        db_table = "post"

    def __str__(self):
        return f"Post ID: {self.Post_ID}"
