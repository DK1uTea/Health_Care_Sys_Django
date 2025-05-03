from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('ADMIN', 'Administrator'),
        ('PHARMACIST', 'Pharmacist'),
        ('INSURANCE', 'Insurance Provider'),
        ('LAB_TECH', 'Laboratory Technician'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'users'

class Permission(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'permissions'

class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission)
    
    class Meta:
        db_table = 'roles'

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'user_roles'
        unique_together = ('user', 'role')