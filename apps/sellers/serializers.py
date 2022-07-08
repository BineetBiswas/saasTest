from apps.sellers.models import Customer, Product, Tier
from rest_framework import serializers




class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    product_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    pricing_link = serializers.URLField(required=True, allow_blank=False)
    product_details = serializers.CharField(required=True, allow_blank=False)
    tiers = serializers.JSONField(required=False)

    def create(self, validated_data):
        return Product.objects.create(**validated_data) 

     
    def update(self, instance, validated_data):
        instance.product_name = validated_data.get('product_name', instance.product_name)
        instance.pricing_link = validated_data.get('pricing_link', instance.pricing_link)
        instance.product_details = validated_data.get('product_details', instance.product_details)
        # instance.tiers = validated_data.get('tiers', instance.tiers)
        instance.save()
        return instance

class TierSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    tier_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    amount = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return Tier.objects.create(**validated_data) 

     
    def update(self, instance, validated_data):
        instance.tier_name = validated_data.get('tier_name', instance.tier_name)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()
        return instance




class CustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    last_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    buyer_email = serializers.EmailField(required=True, allow_blank=False, max_length=255)
    company_name = serializers.CharField(required=True)
    phone= serializers.CharField(required=True)
    


    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.buyer_email = validated_data.get('buyer_email', instance.buyer_email)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.phone=validated_data.get('phone', instance.phone)
        instance.save()
        return instance

class OrderSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)
    tier_id = serializers.IntegerField(required=True)
    price = serializers.IntegerField(required=True)
    special_instruction = serializers.CharField(max_length=200)
    


    def create(self, validated_data):
        return Product.objects.create(**validated_data) 

    def update(self, instance, validated_data):
        instance.customer_id = validated_data.get('customer_id', instance.customer_id)
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.tier_id = validated_data.get('tier_id', instance.tier_id)
        instance.price = validated_data.get('price', instance.price)
        instance.special_instruction = validated_data.get('special_instruction', instance.special_instruction)
        instance.save()
        return instance

class RBACSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    last_name = serializers.CharField(required=True, allow_blank=False, max_length=200)
    email_id = serializers.EmailField(required=True, allow_blank=False, max_length=255)
    role = serializers.CharField(required=True)
    
    


    # def create(self, validated_data):
    #     return Product.objects.create(**validated_data) 