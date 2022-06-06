from apps.kyb.models import BankDetail, BusinessDetail, Company, Product, Profile
from rest_framework import serializers




class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [field.name for field in model._meta.fields]



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [field.name for field in model._meta.fields]

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