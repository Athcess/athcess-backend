from django.db import models

class HaveProfilePic(models.Model):
    #User_ID = models.ForeignKey('User', on_delete=models.CASCADE)
    #Object_ID = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = "HaveProfilePic"

    def __str__(self):
        return f"{self.User_ID} has {self.Object_ID}'s profile picture"
