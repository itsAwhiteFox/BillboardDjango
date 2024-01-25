from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from customers.models import Customer

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if "company" not in extra_fields:
            raise ValueError('The company field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff = False, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staff(self, email = None, password = None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff = True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(unique=True)
    company = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, blank=True, related_name="user_entity")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_by = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name="user_created_by")
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'phone']

    def __str__(self):
        return f"{self.email} {self.is_staff}"
