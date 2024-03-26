from django.db import models

class IsVerified(models.Model):
    #Verified_ID = models.AutoField(primary_key=True)
    #User_ID = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = "is_verified"

    def __str__(self):
        return f"Verification status for User {self.User_ID}"
