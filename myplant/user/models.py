from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser): 
    nickname = models.CharField(max_length=100, default="익명")
    location = models.CharField(max_length=100)