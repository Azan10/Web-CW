from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    profile_image = models.ImageField(upload_to='profile_images/', default='default.jpg', blank=True)
    email = models.EmailField(blank=True, null=True)  

    date_of_birth = models.DateField(null=True, blank=True)
