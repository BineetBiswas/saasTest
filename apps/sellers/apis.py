from apps.sellers.permissions import CompanyPermission
from apps.sellers.serializers import ProductSerializer, TierSerializer
from apps.sellers.models import Product, Tier
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction





class ProductView(APIView):
    permission_classes = [IsAuthenticated, CompanyPermission]

    def get(self, request, format=None):
        if 'id' in request.GET:
            id=request.query_params["id"]
            # id = self.kwargs["id"]
            if id != None and Product.objects.filter(id=id).exists():
                product = Product.objects.get(id=id)
                self.check_object_permissions(request, product)
                serializer= ProductSerializer(product)
            else:
                return Response({"message": "id not recognized"})
        else:
            products = Product.objects.filter(company=request.user.company)
            serializer=ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        serializer=ProductSerializer(data = data)
        

        if serializer.is_valid():
                product_name=serializer.validated_data['product_name']
                product_details=serializer.validated_data['product_details']
                pricing_link=serializer.validated_data['pricing_link']
                tiers=serializer.validated_data['tiers']
                company = request.user.company
                product_obj=Product(
                    company = company, 
                    product_name = product_name,
                    product_details = product_details,
                    pricing_link= pricing_link)
                    # tiers=tiers)
                with transaction.atomic():
                    product_obj.save()
                    product = Product.objects.get(id=product_obj.id)
                
                    for tier in tiers:
                        serializerB= TierSerializer(data=tier)
                        if serializerB.is_valid():
                            serializerB.save(company=company, product=product)
                        else:
                            transaction.set_rollback(True)
                            return Response(serializerB.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        data = request.data
        user = request.user
        
        id=request.query_params["id"]
        if id != None and Product.objects.filter(id=id).exists():
            obj = Product.objects.get(id=id)
            self.check_object_permissions(request, obj)
            serializer=ProductSerializer(obj, data=data, partial=True)
            
            # old_tiers = obj.tier_set.all().values()
            # print(old_tiers)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Product id not recognized"})

    def delete(self, request, format=None):
        id=request.query_params["id"]
        if id != None and Product.objects.filter(id=id).exists():
            obj = Product.objects.get(id=id)
            self.check_object_permissions(request, obj)
            obj.delete()
            return Response({"message": f"Product {id} has been deleted"})
        return Response({"message": "Product id not recognized"})
        
        
class TierView(APIView):
    permission_classes = [IsAuthenticated, CompanyPermission]

    
    def get(self, request, format=None):
        if 'tier_id' in request.GET:
            tier_id=request.query_params["tier_id"]
            if tier_id != None and Tier.objects.filter(id=tier_id).exists():
                tier = Tier.objects.get(id=tier_id)
                self.check_object_permissions(request, tier)
                serializer= TierSerializer(tier)
            else:
                return Response({"message": "tier_id not recognized"})
        elif 'product_id' in request.GET:
            product_id=request.query_params["product_id"]
            # id = self.kwargs["id"]
            if product_id != None and Product.objects.filter(id=product_id).exists():
                product=Product.objects.get(id=product_id)
                self.check_object_permissions(request, product)
                tiers = p.tier_set.all().values()
                print(tiers)
                serializer= TierSerializer(tiers, many = True)
        
            else:
                return Response({"message": "product_id not recognized"})
            
        else:
            if Product.objects.filter(company=request.user.company).exists():
                tiers=[]
                products=Product.objects.filter(company=request.user.company).values()
                for product in products:
                    p = Product.objects.get(id=product['id'])
                    tiers.append(p.tier_set.all().values())
                tiers_cleaned = [x for x in tiers if x]
                result={'data': tiers_cleaned}
                return Response(result)
            else:
                return Response({"message": "No products found for this company"})
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def put(self, request, format=None):
        data = request.data
        user = request.user
        
        id=request.query_params["id"]
        if id != None and Tier.objects.filter(id=id).exists():
            obj = Tier.objects.get(id=id)
            self.check_object_permissions(request, obj)
            serializer=TierSerializer(obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Tier id not recognized"})

    def delete(self, request, format=None):
        id=request.query_params["id"]
        if id != None and Tier.objects.filter(id=id).exists():
            obj = Tier.objects.get(id=id)
            self.check_object_permissions(request, obj)
            obj.delete()
            return Response({"message": f"Tier {id} has been deleted"})
        return Response({"message": "Tier id not recognized"})