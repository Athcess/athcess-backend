from django.db import models
from users.models.custom_user import CustomUser


class PhysicalAttribute(models.Model):
    created_at = models.DateTimeField(primary_key=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    fat_mass = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    muscle_mass = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    run = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    push_up = models.IntegerField(blank=True, null=True)
    sit_up = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "physical_attribute"
    
    def __str__(self):
        return (self.date)

