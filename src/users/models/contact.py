# from django.db import models
# from .custom_user import CustomUser as User


# class Contact(models.Model):
#     user_id = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
#     email = models.EmailField(primary_key=True)
#     phone = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user_id.name
