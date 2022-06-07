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

class BusinessDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDetail
        fields = [field.name for field in model._meta.fields]

class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = [field.name for field in model._meta.fields]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [field.name for field in model._meta.fields]


class Kyb_Gstin_Check(serializers.Serializer):
    gstin    = serializers.CharField(required=True, allow_blank=False, max_length=100)

class Kyb_Cin_Check(serializers.Serializer):
    cin    = serializers.CharField(required=True, allow_blank=False, max_length=100)