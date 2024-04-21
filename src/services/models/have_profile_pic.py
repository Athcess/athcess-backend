from django.db import models
from .blob_storage import BlobStorage
from users.models.custom_user import CustomUser


class HaveProfilePic(models.Model):
    username = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE)
    profile_picture = models.ForeignKey(BlobStorage, on_delete=models.CASCADE)

    class Meta:
        db_table = "have_profilepic"
        indexes = [
            models.Index(fields=['username', 'profile_picture']),
        ]

    def __str__(self):
        return f"{self.User_ID} has {self.Object_ID}'s profile picture"
