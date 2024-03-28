from django.db import models
from .verified import Verified

class IsVerified(models.Model):
    Verified_ID = models.ForeignKey(Verified, primary_key=True, on_delete=models.CASCADE)
    #User_ID = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = "is_verified"

    def __str__(self):
        return f"Verification status for User {self.User_ID}"
