from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)

    # additional
    portfolio_site = models.URLField(blank = True)  # leaving this field blank is accepted

    # If you are working with Images do pip install pillow
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)  # user don't have to upload his profile pic


    def __str__(self):
        return self.user.username
