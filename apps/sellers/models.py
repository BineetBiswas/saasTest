from django.db import models

from apps.kyb.models import Company


# Create your models here.
class Product(models.Model):
    
    company = models.ForeignKey(Company,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)
    product_name = models.CharField(max_length=50, null=True)
    # order_name = models.CharField(max_length=200, null=True, blank=True)
    product_details = models.CharField(max_length=200, null=True, blank=True)
    pricing_link = models.CharField(max_length=255, null=True)
    # tiers = models.JSONField(null=True)
    

    

    def __str__(self):
        return str(self.product_name)


class Tier(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)
    tier_name = models.CharField(max_length=200, null=True, blank=True)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.tier_name)



class Subsription(models.Model):
    
    product = models.ForeignKey(Company,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    subscription_name = models.CharField(max_length=50, null=True)
    # order_name = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    

    

    def __str__(self):
        return str(self.product)


class Customer(models.Model):
    
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    # order_name = models.CharField(max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True)
    phone_no = models.CharField(max_length=200, null=True)

    

    

    def __str__(self):
        return str(self.id)


class InviteToBuyer(models.Model):
    company = models.ForeignKey(Company,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    

    def __str__(self):
        return str(self.company) 