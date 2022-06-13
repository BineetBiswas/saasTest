from apps.sellers.models import Product, Tier
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