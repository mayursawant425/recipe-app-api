from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionMixin


class UserManager(BaseUserManager):
    """Manages User model"""

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves new user"""

        if not email:
            raise valueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(eamil, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionMixin):
    """Custom user model that supports email instead of username"""

    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
