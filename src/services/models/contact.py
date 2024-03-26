from django.db import models

class Contact(models.Model):
    email = models.CharField(primary_key=True, max_length=50)
    # user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)

    class Meta:
        db_table = "contact"

    def __str__(self):
        return self.email