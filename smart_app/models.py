from django.db import models

# Create your models here.
from io import BytesIO
from django.core.files.images import ImageFile
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser
from barcode import generate
from barcode.writer import ImageWriter

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a CustomUser with the given username, email, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username, email, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='student_images/', blank=True, null=True)
    admission_number = models.CharField(max_length=10, unique=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(default=None, null=True)
    blood_group = models.CharField(max_length=3)
    place = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    batch = models.CharField(max_length=10)
    start_year = models.IntegerField(null=True)
    end_year = models.IntegerField(null=True)
    barcode = models.ImageField(upload_to='student_barcodes/', blank=True, null=True)
    objects=CustomUserManager()
    def has_perm(self, perm, obj=None):
        return self.is_staff
    def has_module_perms(self, app_label):
        return self.is_staff

    # groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)  # Added blank=True
    # user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)  # Added blank=True

    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is being created
            if not self.is_superuser:  # Generate barcode only if the user is not a superuser
                barcode_data = self.admission_number
                barcode_image = BytesIO()
                generate('code128', barcode_data, writer=ImageWriter(), output=barcode_image)
                barcode_image.seek(0)
                self.barcode.save(f"{self.admission_number}.png", ImageFile(barcode_image, name=f"{self.admission_number}.png"), save=False)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user_a')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.admission_number} - {self.timestamp}"