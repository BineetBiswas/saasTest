from apps.sellers.serializers import ProductSerializer
from apps.sellers.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny





class ProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            id=request.query_params["id"]
            # id = self.kwargs["id"]
            if id != None and Product.objects.filter(id=id).exists():
                product = Product.objects.get(id=id)
                serializer= ProductSerializer(product)
            else:
                return Response({"message": "id not recognized"})
        except:
            products = Product.objects.filter(company=request.user.company)
            serializer=ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        serializer=ProductSerializer(data = data)

        if serializer.is_valid():
                serializer.save(company=request.user.company)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        data = request.data
        user = request.user
        id=request.query_params["id"]
        if id != None and Product.objects.filter(id=id).exists():
            obj = Product.objects.get(id=id)
            serializer=ProductSerializer(obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "id not recognized"})

    def delete(self, request, format=None):
        id=request.query_params["id"]
        if id != None and Product.objects.filter(id=id).exists():
            obj = Product.objects.get(id=id)
            obj.delete()
            return Response({"message": f"{id} has been deleted"})
        return Response({"message": "id not recognized"})
        
        