from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import os


# Create your models here.
class CustomUser(AbstractUser):
    ADMIN=1
    USERS=2
    Roll_Choices=(
        (ADMIN,'admin'),
        (USERS,'user'),
    )
    user_role = models.PositiveSmallIntegerField(choices=Roll_Choices,default=ADMIN)
    mobile_no = models.CharField(max_length=50,blank=False)
    def path_and_rename(self, filename):
        upload_to = 'user_profile'
        ext = filename.split('.')[-1]
        if self.username:
            filename = '{}-{}.{}'.format(self.username, datetime.date.today(), ext)

        return os.path.join(upload_to, filename)
    
    user_profile = models.ImageField(upload_to=path_and_rename, default=False)
    is_verified = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)

    updated_on = models.DateTimeField(auto_now=True)
