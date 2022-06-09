from apps.kyb.models import BankDetail, BusinessDetail, Company, Product, Profile
from rest_framework import serializers




class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [field.name for field in model._meta.fields]






class ProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    last_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    email = serializers.EmailField(required=True, allow_blank=False, max_length=255)
    phone_number = serializers.IntegerField(required=True)
    designation = serializers.CharField(required=True, allow_blank=False, max_length=200)
    industry = serializers.CharField(required=True, allow_blank=False, max_length=200)
    business_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    annual_revenue=serializers.IntegerField(required=True)
    
    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.designation = validated_data.get('designation', instance.designation)
        instance.industry = validated_data.get('industry', instance.industry)
        instance.business_name = validated_data.get('business_name', instance.business_name)
        instance.annual_revenue = validated_data.get('annual_revenue', instance.annual_revenue)
        instance.save()
        return instance

# class BusinessDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BusinessDetail
#         fields = [field.name for field in model._meta.fields]

# class BankDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BankDetail
#         fields = [field.name for field in model._meta.fields]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [field.name for field in model._meta.fields]


class Kyb_Gstin_Check(serializers.Serializer):
    gstin    = serializers.CharField(required=True, allow_blank=False, max_length=100)

class Kyb_Cin_Check(serializers.Serializer):
    cin    = serializers.CharField(required=True, allow_blank=False, max_length=100)


class BankDetailSerializer(serializers.Serializer):
    bank_name = serializers.CharField(required=True, allow_blank=False, max_length=255)
    branch_name = serializers.CharField(required=True, allow_blank=False, max_length=255)
    ifsc_code = serializers.CharField(required=True, allow_blank=False, max_length=255)
    account_no = serializers.CharField(required=True, allow_blank=False, max_length=255)
    
    
    def create(self, validated_data):
        return BankDetail.objects.create(**validated_data)

class BusinessDetailSerializer(serializers.Serializer):
    GSTIN=serializers.CharField(required=False, allow_blank=True, max_length=50, read_only=True)
    PAN=serializers.CharField(required=False, allow_blank=True, max_length=50, read_only=True)
    CIN=serializers.CharField(required=False, allow_blank=True, max_length=50, read_only=True)
    DIN=serializers.CharField(required=False, allow_blank=True, max_length=50, read_only=True)
    contact_address_Line1 = serializers.CharField(required=True, allow_blank=False, max_length=255)
    contact_address_Line2 = serializers.CharField(required=True, allow_blank=False, max_length=255)
    contact_address_PinCode = serializers.CharField(required=True, allow_blank=False, max_length=10)
    contact_address_State = serializers.CharField(required=True, allow_blank=False, max_length=255)
    contact_address_City = serializers.CharField(required=True, allow_blank=False, max_length=255)
    
    def create(self, validated_data):
        return BankDetail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.GSTIN = validated_data.get('GSTIN', instance.GSTIN)
        instance.PAN = validated_data.get('PAN', instance.PAN)
        instance.CIN = validated_data.get('CIN', instance.CIN)
        instance.DIN = validated_data.get('DIN', instance.DIN)
        instance.contact_address_Line1 = validated_data.get('contact_address_Line1', instance.contact_address_Line1)
        instance.contact_address_Line2 = validated_data.get('contact_address_Line2', instance.contact_address_Line2)
        instance.contact_address_PinCode = validated_data.get('contact_address_PinCode', instance.contact_address_PinCode)
        instance.contact_address_State = validated_data.get('contact_address_State', instance.contact_address_State)
        instance.contact_address_City = validated_data.get('contact_address_City', instance.contact_address_City)
        instance.save()
        return instance