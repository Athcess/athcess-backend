from django.db import models
from .post import Post
from users.models.custom_user import CustomUser


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateField()
    like = models.JSONField(null=True)
    description = models.CharField(max_length=200)

    class Meta:
        db_table = "comment"

    def __str__(self):
        return f"Comment ID: {self.Comment_ID}"
