from django.db import models

class Comment(models.Model):
    Comment_ID = models.AutoField(primary_key=True)
   # User_ID = models.ForeignKey('User', on_delete=models.CASCADE)
    Post_ID = models.ForeignKey('Post', on_delete=models.CASCADE)
    Date = models.DateField()
    Commenter_User_ID = models.CharField(max_length=16)
    Like = models.JSONField(null=True) 
    Comment_Data = models.CharField(max_length=200)

    class Meta:
        db_table = "comment"

    def __str__(self):
        return f"Comment ID: {self.Comment_ID}"
