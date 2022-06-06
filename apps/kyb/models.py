from django.db import models

# Create your models here.



class Company(models.Model):
    
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255, null=True)
    is_kyb_done = models.BooleanField(default=False)
    is_kyc_done = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    def __str__(self):
        return str(self.company_name)



class Profile(models.Model):
    
    company = models.ForeignKey(Company,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=False)
    last_name = models.CharField(max_length=200, null=True, blank=False)
    email = models.CharField(max_length=200, null=True, blank=False)
    phone_number = models.CharField(max_length=122, default="")
    designation = models.CharField(max_length=200, null=True, blank=False)
    industry = models.CharField(max_length=200, null=True, blank=False)
    business_name = models.CharField(max_length=200, null=True, blank=False)
    annual_revenue = models.CharField(max_length=200, null=True, blank=False)
    

    def __str__(self):
        return str(self.email)


class BusinessDetail(models.Model):
    
    company = models.OneToOneField(Company,
                                on_delete=models.CASCADE,
                                primary_key=True)
    GSTIN = models.CharField(max_length=50, null=True)
    # order_name = models.CharField(max_length=200, null=True, blank=True)
    PAN = models.CharField(max_length=200, null=True, blank=True)
    CIN = models.CharField(max_length=200, null=True)
    TAN = models.CharField(max_length=200, null=True)
    phone_number = models.IntegerField(null=True)
    company_address=models.CharField(max_length=255, null=True)
    annual_revenue=models.IntegerField(null=True)
    industry= models.CharField(max_length=255, null=True)

    

    def __str__(self):
        return str(self.GSTIN)


class BankDetail(models.Model):
    
    company = models.OneToOneField(Company,
                                on_delete=models.CASCADE,
                                primary_key=True)
    bank_name = models.CharField(max_length=50, null=True)
    # order_name = models.CharField(max_length=200, null=True, blank=True)
    branch_name = models.CharField(max_length=200, null=True, blank=True)
    ifsc_code = models.CharField(max_length=200, null=True)
    account_no = models.CharField(max_length=200, null=True)
    

    

    def __str__(self):
        return str(self.company)

class Product(models.Model):
    
    company = models.ForeignKey(Company,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    product_name = models.CharField(max_length=50, null=True)
    # order_name = models.CharField(max_length=200, null=True, blank=True)
    product_detail = models.CharField(max_length=200, null=True, blank=True)
    pricing = models.CharField(max_length=200, null=True)
    tiers = models.CharField(max_length=200, null=True)
    

    

    def __str__(self):
        return str(self.product_name)


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