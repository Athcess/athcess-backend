from django.db import models
from users.models.custom_user import CustomUser


class PhysicalAttribute(models.Model):
    date = models.DateTimeField(primary_key=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    height = models.IntegerField()
    speed = models.IntegerField()
    fat_mass = models.DecimalField(max_digits= 4, decimal_places= 2)
    muscle_mass = models.DecimalField(max_digits= 4, decimal_places=2)
    weight = models.DecimalField(max_digits=4, decimal_places= 1)

    class Meta:
        db_table = "physical_attribute"
    
    def __str__(self):
        return (self.date, self.muscle_mass)

