from apps.sellers.permissions import CompanyAdminPermission, CompanyPermission
from apps.sellers.serializers import CustomerSerializer, OrderSerializer, ProductSerializer, RBACSerializer, TierSerializer
from apps.sellers.models import Customer, Order, Product, Tier
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction

from apps.users.models import User
from django.db.models import Q






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



class CustomerView(APIView):
    permission_classes = [IsAuthenticated, CompanyPermission]

    def post(self, request):
        data = request.data
        serializer=CustomerSerializer(data = data)

        if serializer.is_valid():
                first_name = serializer.validated_data['first_name']
                last_name = serializer.validated_data["last_name"]
                buyer_email = serializer.validated_data["buyer_email"]
                domain = buyer_email.split('@')[1]
                company_name = serializer.validated_data["company_name"]
                phone = serializer.validated_data["phone"]
                company = request.user.company
                
                

                if User.objects.filter(email=buyer_email).exists():
                    # cust = Customer.objects.get(id = cust_id)
                    user = User.objects.get(email=buyer_email)
                    if user.company != request.user.company:
                        # setattr(user.company, "is_buyer", True)
                        setattr(user, "kyc_required", True)
                        user.save()
                    
                else:
                    user = User.objects.create(email=buyer_email, first_name = first_name, last_name=last_name, kyc_required=True)
                if Customer.objects.filter(
                Q(buyer=user) & Q(company=request.user.company)).exists():
                    return Response({"message": "Customer already exists in your list"})
                   
                customer = Customer(buyer=user, first_name = first_name, last_name=last_name, email = buyer_email, domain=domain, phone_no=phone, company=company)
                customer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def put(self, request, format=None):
    #     data = request.data
    #     user = request.user
        
    #     id=request.query_params["id"]
    #     if id != None and Customer.objects.filter(id=id).exists():
    #         obj = Customer.objects.get(id=id)
    #         self.check_object_permissions(request, obj)
    #         serializer=CustomerSerializer(obj, data=data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({"message": "Customer id not recognized"})

    def delete(self, request, format=None):
        id=request.query_params["id"]
        if id != None and Customer.objects.filter(id=id).exists():
            obj = Customer.objects.get(id=id)
            self.check_object_permissions(request, obj)
            obj.delete()
            return Response({"message": f"Customer {id} has been deleted"})
        return Response({"message": "Customer id not recognized"})
                




class OrderView(APIView):
    permission_classes = [IsAuthenticated, CompanyPermission]

    def post(self, request):
        data = request.data
        serializer=OrderSerializer(data = data)
        

        if serializer.is_valid():
                

                customer_id = serializer.validated_data["customer_id"]
                product_id = serializer.validated_data["product_id"]
                tier_id = serializer.validated_data["tier_id"]
                
                price = serializer.validated_data["price"]
                instruction= serializer.validated_data["special_instruction"]
                if Customer.objects.filter(id=customer_id).exists():
                    customer = Customer.objects.get(id=customer_id)
                    if customer.company != request.user.company:
                        return Response({"message": "Customer was not added by company"})
                else: 
                    return Response({"message": "Customer does not exist"})
                if Product.objects.filter(id=product_id).exists():
                    product = Product.objects.get(id=product_id)
                    if product.company != request.user.company:
                        return Response({"message": "Product does not belong to company"})
                else: 
                    return Response({"message": "Product does not exist"})
                if Tier.objects.filter(id=tier_id).exists():
                    tier = Tier.objects.get(id=tier_id)
                    if tier.company != request.user.company:
                        return Response({"message": "Tier does not belong to company"})
                else: 
                    return Response({"message": "Tier does not exist"})
                
                order = Order(seller = request.user.company, buyer=customer, product = product, tier=tier, price = price, special_instruction=instruction)
                order.save()  
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    # def put(self, request, format=None):
    #     data = request.data
    #     user = request.user
        
    #     id=request.query_params["id"]
    #     if id != None and Order.objects.filter(id=id).exists():
    #         obj = Order.objects.get(id=id)
    #         self.check_object_permissions(request, obj)
    #         serializer=OrderSerializer(obj, data=data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({"message": "Order id not recognized"})

    def delete(self, request, format=None):
        id=request.query_params["id"]
        if id != None and Order.objects.filter(id=id).exists():
            obj = Order.objects.get(id=id)
            self.check_object_permissions(request, obj)
            obj.delete()
            return Response({"message": f"Order {id} has been deleted"})
        return Response({"message": "Order id not recognized"})



class RBACView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer=RBACSerializer(data = data)
        

        if request.user.email == request.user.company.admin_id:


            if serializer.is_valid():
                    first_name = serializer.validated_data['first_name']
                    last_name = serializer.validated_data["last_name"]
                    email_id = serializer.validated_data["email_id"]
                    role = serializer.validated_data["role"]

                    if User.objects.filter(email=email_id).exists():
                        return Response({"message": "User already exists"})
                    else:
                        User.objects.create(email= email_id, company= request.user.company, first_name=first_name, last_name=last_name, rbac_role=role)
                        return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Only company admin can add other team members"})