from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

from apps.kyb.models import Company
from .manager import UserManager
 




class User(AbstractUser):
    username = None
    email = models.EmailField( unique=True)
    company = models.ForeignKey(Company,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6 , null=True, blank=True)
    activation_key = models.CharField(max_length=150,blank=True,null=True)
    rbac_role = models.CharField(max_length=150,blank=True,null=True)
    kyc_required = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email