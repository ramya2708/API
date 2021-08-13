from django.db import models
from accounts.models import CustomUser

# Create your models here.
class LoginUser(models.Model):
    user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    otp = models.IntegerField()
    country = models.CharField(max_length=100, blank=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

