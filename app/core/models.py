# Create your models here.
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads', 'recipe', filename)

class UserManager(BaseUserManager):
    """Manager for user"""

    def create_user(self, email, password = None, **extra_fields):
        """Create and save a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using = self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True) # is_active is required for custom user model
    is_staff = models.BooleanField(default=False) # is_staff is required for custom user model
    objects = UserManager()
    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    link = models.CharField(max_length=255, blank = True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null = True, upload_to = recipe_image_file_path)

    def __str__(self):
        return self.title

class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.name

