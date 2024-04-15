from django.db import models
from .post import Post
from .is_verified import IsVerified as Verified
from .physical_attribute import PhysicalAttribute
from users.models.custom_user import CustomUser, Organization


class BlobStorage(models.Model):
    blob_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    is_profile_picture = models.BooleanField(default=False)
    verify = models.ForeignKey(Verified, on_delete=models.CASCADE, blank=True, null=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    club_name = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True)
    physical_attribute = models.ForeignKey(PhysicalAttribute, on_delete=models.CASCADE, blank=True, null=True)
    content_type = models.CharField(max_length=30)
    description = models.CharField(max_length=30,blank=True, null=True)
    url = models.TextField(max_length=250)
    file_name = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=[('pending', 'Pending'), ('uploaded', 'Uploaded'), ('failed', 'Failed')])
    file_size = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    skill_type = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = "blob_storage"

    def __str__(self):
        return f"BlobStorage object: {self.blob_id}"
