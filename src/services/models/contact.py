from django.db import models
from users.models.custom_user import CustomUser


class Contact(models.Model):
    email = models.CharField(primary_key=True, max_length=50)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)

    class Meta:
        db_table = "contact"

    def __str__(self):
        return self.email