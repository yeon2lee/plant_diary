from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser): 
    nickname = models.CharField(max_length=100, default="익명")
    location = models.CharField(max_length=100, blank=True)
    followers = models.ManyToManyField(
            settings.AUTH_USER_MODEL,
            related_name='followings'
        )
