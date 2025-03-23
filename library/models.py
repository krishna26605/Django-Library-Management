from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

class AdminUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email instead of username."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class AdminUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None  # Remove username requirement
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = AdminUserManager()  # Use the custom manager

    groups = models.ManyToManyField(Group, related_name="admin_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="admin_users_permissions", blank=True)

    def __str__(self):
        return self.email

# ✅ Added the missing Book model  
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
