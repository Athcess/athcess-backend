from django.db import models
from .post import Post
from .is_verified import IsVerified as Verified
from .physical_attribute import PhysicalAttribute as PhyAtr

class BlobStorage(models.Model):
    Object_ID = models.AutoField(primary_key=True)
    Post_ID = models.ForeignKey(Post, on_delete=models.CASCADE)
    Vefified_ID = models.ForeignKey(Verified, on_delete=models.CASCADE)
    #Org_Name = models.ForeignKey('OrgName', on_delete=models.CASCADE)
    #Athlete_User_ID = models.ForeignKey('User', on_delete=models.CASCADE)
    Date = models.ForeignKey(PhyAtr, on_delete= models.CASCADE)
    Type = models.CharField(max_length=30, choices=[('type1', 'Type 1'), ('type2', 'Type 2'), ('type3', 'Type 3')])
    Description = models.CharField(max_length=30)
    Url = models.CharField(max_length=100)
    Skill_type = models.CharField(max_length=30, choices=[('skill1', 'Skill 1'), ('skill2', 'Skill 2'), ('skill3', 'Skill 3')])

    class Meta:
        db_table = "blob_storage"

    def __str__(self):
        return f"BlobStorage object: {self.Object_ID}"
