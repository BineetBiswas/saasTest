from apps.kyb.models import BusinessDetail, Company, Profile
from apps.kyb.serializers import CompanySerializer, Kyb_Cin_Check, Kyb_Gstin_Check, ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
import requests
import json
import os





class KybProfile(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer=ProfileSerializer(data = data)

        if serializer.is_valid():
            if not Profile.objects.filter(created_by=request.user).exists():
                serializer.save(created_by=request.user)
                
                return Response(data, status=status.HTTP_200_OK)
            return Response({'message': "User has already created a profile"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KybGstinCheck(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer=Kyb_Gstin_Check(data=data)
        user = request.user
        

        if serializer.is_valid():
            gstin = serializer.validated_data['gstin']

            url = "https://in.staging.decentro.tech/kyc/public_registry/validate"

            payload = json.dumps({
            "reference_id": "0000-0000-0000-2004",
            "document_type": "GSTIN",
            "id_number": gstin,
            "consent": "Y",
            "consent_purpose": "For bank account purpose only"
            })
            headers = {
            'client_id': os.environ.get('client_id'),
            'client_secret': os.environ.get('client_secret'),
            'module_secret': os.environ.get('module_secret'),
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            result = json.loads(response.text)
            if result['kycStatus']=='SUCCESS':
        
                pan = result['kycResult']['pan']
                name = result['kycResult']['legalName']
                
                
                if not Company.objects.filter(company_name=name).exists():
                    company = Company(company_name=name)
                    company.save()
                business = Company.objects.get(company_name=name)
                if not BusinessDetail.objects.filter(company=business).exists():
                    BusinessDetail.objects.create(company = business, GSTIN = gstin, PAN = pan)
                setattr(user, 'company', business)
                user.save()
                profile=Profile.objects.get(created_by=user)
                setattr(profile, 'company', business)
                profile.save()

                res = {
                    'status': 200,
                    'message': result['kycStatus'],
                    'pan': pan
                }
                return Response(res, status=status.HTTP_200_OK)
            
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

            

class KybCinCheck(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer=Kyb_Cin_Check(data=data)
        user = request.user
        

        if serializer.is_valid():
            cin = serializer.validated_data['cin']

            url = "https://in.staging.decentro.tech/kyc/public_registry/validate"

            payload = json.dumps({
            "reference_id": "0000-0000-0000-2005",
            "document_type": "CIN",
            "id_number": cin,
            "consent": "Y",
            "consent_purpose": "For bank account purpose only"
            })
            headers = {
            'client_id': os.environ.get('client_id'),
            'client_secret': os.environ.get('client_secret'),
            'module_secret': os.environ.get('module_secret'),
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            result = json.loads(response.text)
            print(type(result))
            status = result.get("kycStatus")
            if not status:
        
                din = result['kycResult']['directors'][0]['dinOrPan']
                address = result['kycResult']['companyMasterData']['registeredAddress']
                
                business = BusinessDetail.objects.get(request.user.company)
                setattr(business, 'DIN', din)
                setattr(business, 'company_address', address)
                business.save()

                res = {
                    'status': 200,
                    'message': result['kycStatus'],
                    'DIN': din,
                    'RegisteredAddress': address
                }
                return Response(res, status=status.HTTP_200_OK)
            
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)