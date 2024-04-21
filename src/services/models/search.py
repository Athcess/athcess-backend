from django.db import models


class Search(models.Model):
    search_id = models.AutoField(primary_key=True)
    data = models.JSONField()

    class Meta:
        db_table = "search"

    def __str__(self):
        return f"{self.search_id}"
