from django.db import models
from django.conf import settings


# Create your models here.



class Company(models.Model):
    
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255, null=True)
    domain=models.CharField(max_length=200, null=True)
    admin_id = models.EmailField(max_length=200, null=True)
    is_kyb_done = models.BooleanField(default=False)
    is_kyc_done = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    def __str__(self):
        return str(self.company_name)



class Profile(models.Model):
    
    company = models.OneToOneField(Company,
                                 on_delete=models.CASCADE,
                                 null=True,
                                )
    first_name = models.CharField(max_length=200, null=True, blank=False)
    last_name = models.CharField(max_length=200, null=True, blank=False)
    email = models.CharField(max_length=200, null=True, blank=False)
    phone_number = models.IntegerField(null=True, blank=False)
    designation = models.CharField(max_length=200, null=True, blank=False)
    industry = models.CharField(max_length=200, null=True, blank=False)
    business_name = models.CharField(max_length=200, null = True, blank=False)
    annual_revenue=models.IntegerField(null=True, blank=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    

    def __str__(self):
        return str(self.email)


class BusinessDetail(models.Model):
    
    company = models.OneToOneField(Company,
                                on_delete=models.CASCADE,
                                primary_key=True)
    GSTIN = models.CharField(max_length=50, null=True)
    # order_name = models.CharField(max_length=200, null=True, blank=True)
    PAN = models.CharField(max_length=200, null=True)
    CIN = models.CharField(max_length=200, null=True)
    DIN = models.CharField(max_length=200, null=True)
    TAN = models.CharField(max_length=200, null=True)
    # phone_number = models.IntegerField(null=True)
    company_registered_address=models.CharField(max_length=255, null=True)
    contact_address_Line1= models.CharField(max_length=255, null=True)
    contact_address_Line2= models.CharField(max_length=255, null=True)
    contact_address_PinCode= models.CharField(max_length=255, null=True)
    contact_address_State= models.CharField(max_length=255, null=True)
    contact_address_City= models.CharField(max_length=255, null=True)

    # annual_revenue=models.IntegerField(null=True)
    # industry= models.CharField(max_length=255, null=True)

    

    def __str__(self):
        return str(self.GSTIN)


class BankDetail(models.Model):
    
    company = models.OneToOneField(Company,
                                on_delete=models.CASCADE,
                                primary_key=True)
    bank_name = models.CharField(max_length=255, null=True)
    # order_name = models.CharField(max_length=200, null=True, blank=True)
    branch_name = models.CharField(max_length=255, null=True, blank=True)
    ifsc_code = models.CharField(max_length=255, null=True)
    account_no = models.CharField(max_length=255, null=True)
    

    

    def __str__(self):
        return str(self.company)

