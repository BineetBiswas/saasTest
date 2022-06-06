from apps.kyb.models import Company
from apps.kyb.serializers import CompanySerializer, ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny





class KybProfile(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        print(request.user)
        # serializerA=CompanySerializer
        serializer=ProfileSerializer(data = data)

        if serializer.is_valid():
            
            business_name = serializer.validated_data['business_name']
            if not Company.objects.filter(company_name=business_name).exists():
                company = Company(company_name=business_name)
                company.save()
                id = Company.objects.get(company_name=business_name)
                serializer.save(company=id)
                
                return Response(data, status=status.HTTP_200_OK)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

       