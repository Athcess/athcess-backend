from django.db import models

class PhysicalAttribute(models.Model):
    date = models.DateTimeField(primary_key=True)
    # user_id = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
    height = models.IntegerField()
    speed = models.IntegerField()
    fat_mass = models.DecimalField(max_digits= 4, decimal_places= 2)
    muscle_mass = models.DecimalField(max_digits= 4, decimal_places=2)
    weight = models.DecimalField(max_digits=4, decimal_places= 1)

    class Meta:
        db_table = "physical_attribute"
    
    def __str__(self):
        return (self.date, self.muscle_mass)

