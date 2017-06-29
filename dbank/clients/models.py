from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Client(AbstractUser):
    phone_number = models.CharField('phone number', max_length=64, null=True)

    def __str__(self):
        return self.get_full_name().title()