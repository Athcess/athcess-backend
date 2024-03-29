from django.db import models


class Model(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "model"

    def __unicode__(self):
        return str(self.id)


from django.db import models

# Create your models here.
