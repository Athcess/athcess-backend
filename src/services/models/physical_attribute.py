from django.db import models
from users.models.custom_user import CustomUser


class PhysicalAttribute(models.Model):
    date = models.DateTimeField(primary_key=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    height = models.IntegerField()
    weight = models.DecimalField(max_digits=4, decimal_places= 1)
    fat_mass = models.DecimalField(max_digits= 4, decimal_places= 2)
    muscle_mass = models.DecimalField(max_digits= 4, decimal_places=2)
    run = models.DecimalField(blank=True, null=True, max_digits= 4, decimal_places=2)
    push_up = models.IntegerField(blank=True, null=True)
    sit_up = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "physical_attribute"
    
    def __str__(self):
        return (self.date, self.muscle_mass)

