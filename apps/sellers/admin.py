from django.contrib import admin

# Register your models here.
from apps.sellers.models import Customer, InviteToBuyer, Order, Product, Tier


admin.site.register(Product)
admin.site.register(Tier)
admin.site.register(Customer)
admin.site.register(InviteToBuyer)
admin.site.register(Order)