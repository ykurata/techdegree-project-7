from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,
                                related_name="current_user",
                                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    verify_email = models.EmailField(max_length=100)
    birth_date = models.DateField()
    bio = models.TextField(default="")
    avatar = models.ImageField(upload_to="profile_image/", blank=True)

    def __str__(self):
        return self.first_name
