from django.db import models
from .verified import Verified
from users.models.custom_user import CustomUser

class IsVerified(models.Model):
    verify = models.OneToOneField(Verified, primary_key=True, on_delete=models.CASCADE)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)


    class Meta:
        db_table = "is_verified"

    def __str__(self):
        return f"Verification status for User {self.username}"
