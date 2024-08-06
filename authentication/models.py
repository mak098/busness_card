from django.db import models

from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):

    class Meta:
        verbose_name_plural = "Utilisateurs"
        db_table = "users"




