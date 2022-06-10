from django.contrib import admin

from apps.kyb.models import BankDetail, BusinessDetail, Company, Profile
# from .models import *
# Register your models here.

admin.site.register(Company)
admin.site.register(BusinessDetail)
admin.site.register(Profile)
admin.site.register(BankDetail)
