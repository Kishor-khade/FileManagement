from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)

class Document(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Staff(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='staffs')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


