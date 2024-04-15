from django.contrib.postgres.fields import ArrayField
from django.db import models
from users.models.custom_user import CustomUser


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    description = models.TextField()
    has_attachment = models.BooleanField()
    likes = models.TextField(default='')  # Field to store a comma-separated list of usernames
    highlight = models.BooleanField(default=False)

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
            return {'message': 'Post liked successfully'}

        updated_likes = [name for name in self.likes.split(',') if name != username]
        self.likes = ','.join(updated_likes)
        self.save()
        return {'message': 'Post unliked successfully'}


    class Meta:
        db_table = "post"

    def __str__(self):
        return f"Post ID: {self.post_id}"
