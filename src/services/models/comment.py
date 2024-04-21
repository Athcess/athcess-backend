from django.db import models
from .post import Post
from users.models.custom_user import CustomUser


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    likes = models.TextField(default='')  # Field to store a comma-separated list of usernames
    description = models.CharField(max_length=200)

    def like(self, username):
        """
        Add a username to the list of likes for this post.
        """
        if username not in self.likes.split(','):
            if self.likes:
                self.likes += f',{username}'
            else:
                self.likes = username
            self.save()
            return {'message': 'Comment liked successfully'}

        updated_likes = [name for name in self.likes.split(',') if name != username]
        self.likes = ','.join(updated_likes)
        self.save()
        return {'message': 'Comment unliked successfully'}

    class Meta:
        db_table = "comment"
        indexes = [
            models.Index(fields=['comment_id', 'username']),
        ]

    def __str__(self):
        return f"Comment ID: {self.comment_id}"
