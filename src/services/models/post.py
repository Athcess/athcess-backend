from django.contrib.postgres.fields import ArrayField
from django.db import models
from users.models.custom_user import CustomUser


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    description = models.TextField()
    like = ArrayField(models.IntegerField(), default=list)

    class Meta:
        db_table = "post"

    def __str__(self):
        return f"Post ID: {self.Post_ID}"
