from django.db import models
from .post import Post
from .is_verified import IsVerified as Verified
from .physical_attribute import PhysicalAttribute
from users.models.custom_user import CustomUser, Organization


class BlobStorage(models.Model):
    blob_id = models.AutoField(primary_key=True, blank=True, null=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    verify_id = models.ForeignKey(Verified, on_delete=models.CASCADE, blank=True, null=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    club_name = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
    physical_attribute = models.ForeignKey(PhysicalAttribute, on_delete= models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=30, choices=[('type1', 'Type 1'), ('type2', 'Type 2'), ('type3', 'Type 3')])
    description = models.CharField(max_length=30)
    url = models.CharField(max_length=100)
    skill_type = models.CharField(max_length=30, choices=[('skill1', 'Skill 1'), ('skill2', 'Skill 2'), ('skill3', 'Skill 3')])

    class Meta:
        db_table = "blob_storage"

    def __str__(self):
        return f"BlobStorage object: {self.blob_id}"
