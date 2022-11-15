from django.contrib.auth.models import AbstractUser
from django.db import models

from user_app.manager import UserManager


class User(AbstractUser):
    """User model."""

    username = None
    first_name = None
    last_name = None
    is_staff = None
    full_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, unique=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        db_table = 'USERS'

