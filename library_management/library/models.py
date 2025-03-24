from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

class AdminUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email instead of username."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)  # Ensure users are active by default
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email, password, **extra_fields)

class AdminUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None  # Remove username requirement
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = AdminUserManager()  # Use the custom manager

    groups = models.ManyToManyField(Group, related_name="admin_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="admin_users_permissions", blank=True)

    def __str__(self):
        return self.email

# ✅ Improved Book model with verbose names and better defaults
class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Book Title")
    author = models.CharField(max_length=255, verbose_name="Author")
    published_date = models.DateField(verbose_name="Publication Date")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    available = models.BooleanField(default=True, verbose_name="Available")

    def __str__(self):
        return self.title