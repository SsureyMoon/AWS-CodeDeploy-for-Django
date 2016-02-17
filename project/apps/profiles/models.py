from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager

from core.utils import GenerateRandomFilename


image_dir = "profiles"
allowed_ext = ['png', 'jpeg', 'jpg', 'gif', 'bmp']
generate_random_filename = GenerateRandomFilename(image_dir, allowed_ext=allowed_ext)

class User(AbstractUser):

    # common
    profile_img = models.ImageField(upload_to=generate_random_filename, blank=True, null=True)

    def __unicode__(self):
        return self.username

    @property
    def profile_img_url(self):
        if self.profile_img and self.profile_img.url:
            return self.profile_img.url

        return settings.MEDIA_URL + "%s/empty_user_profile_img.png" % (image_dir,)
    