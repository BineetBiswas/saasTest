from django.contrib import admin

from apps.kyb.models import BankDetail, BusinessDetail, Company, Customer, InviteToBuyer, Product, Profile, Subsription
# from .models import *
# Register your models here.

admin.site.register(Company)
admin.site.register(BusinessDetail)
admin.site.register(Profile)
admin.site.register(BankDetail)
admin.site.register(Product)
admin.site.register(Subsription)
admin.site.register(Customer)
admin.site.register(InviteToBuyer)