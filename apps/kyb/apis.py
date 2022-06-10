from apps.kyb.models import BankDetail, BusinessDetail, Company, Profile
from apps.kyb.serializers import BankDetailSerializer, BusinessDetailSerializer, CompanySerializer, Kyb_Cin_Check, Kyb_Gstin_Check, ProfileSerializer
from apps.kyb.utils import decentroAPI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.renderers import JSONRenderer
import requests
import json
import os





class KybProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        print(request.user.id)
        if not Profile.objects.filter(created_by=request.user).exists():
            return Response({'message': "No profile associated with user"}, status=status.HTTP_400_BAD_REQUEST)
        profile= Profile.objects.get(created_by=request.user)
        print(profile.id)
        serializer= ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer=ProfileSerializer(data = data)

        if serializer.is_valid():
            if not Profile.objects.filter(created_by=request.user).exists():
                serializer.save(created_by=request.user)
                
                return Response(data, status=status.HTTP_200_OK)
            return Response({'message': "User has already created a profile"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        data = request.data
        user = request.user
        if Profile.objects.filter(company=user.company).exists():
            obj = Profile.objects.get(company=user.company)
            serializer=BusinessDetailSerializer(obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No account found'}, status=status.HTTP_400_BAD_REQUEST)


class KybGstinCheck(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer=Kyb_Gstin_Check(data=data)
        user = request.user
        type = "GSTIN"

        if serializer.is_valid():
            gstin = serializer.validated_data['gstin']

            result = decentroAPI(type, gstin)
            if result['kycStatus']=='SUCCESS':
        
                pan = result['kycResult']['pan']
                name = result['kycResult']['legalName']
                address=result['kycResult']['primaryBusinessContact']['address']
                
                
                if not Company.objects.filter(company_name=name).exists():
                    company = Company(company_name=name)
                    company.save()
                business = Company.objects.get(company_name=name)
                setattr(user, 'company', business)
                user.save()
                if not Profile.objects.filter(created_by=user).exists():
                    return Response({'message': "User does not have a profile"}, status=status.HTTP_400_BAD_REQUEST)
                profile=Profile.objects.get(created_by=user)
                setattr(profile, 'company', business)
                profile.save()
                if not BusinessDetail.objects.filter(company=business).exists():
                    BusinessDetail.objects.create(company = business, GSTIN = gstin, PAN = pan)

                    res = {
                        'status': 200,
                        'message': result['kycStatus'],
                        'pan': pan,
                        'address': address
                    }
                    return Response(res, status=status.HTTP_200_OK)
                return Response({'message': "Existing GSTIN and PAN cannot be updated."}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

            

class KybCinCheck(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer=Kyb_Cin_Check(data=data)
        user = request.user
        type = "CIN"
        

        if serializer.is_valid():
            cin = serializer.validated_data['cin']

            result = decentroAPI(type, cin)
            print(type(result))
            status = result.get("kycStatus")
            if not status:
        
                din = result['kycResult']['directors'][0]['dinOrPan']
                address = result['kycResult']['companyMasterData']['registeredAddress']
                
                if not BusinessDetail.objects.filter(company=user.company).exists():
                    pass
                business = BusinessDetail.objects.get(company = user.company)
                setattr(business, 'DIN', din)
                setattr(business, 'company_registered_address', address)
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


class KybBankDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if not BankDetail.objects.filter(company=request.user.company).exists():
            return Response({'message': "No banking details available for this user"}, status=status.HTTP_400_BAD_REQUEST)
        details= BankDetail.objects.get(company=request.user.company)
        serializer= BankDetailSerializer(details)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer=BankDetailSerializer(data=data)
        user = request.user
        company = user.company

        if serializer.is_valid():
            if not BankDetail.objects.filter(company=company).exists():
                serializer.save(company=company)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'message': "Bank Details already exist for this user"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KybBusinessDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        if BusinessDetail.objects.filter(company=user.company).exists():
            obj = BusinessDetail.objects.get(company=user.company)
            serializer=BusinessDetailSerializer(data=data)
            if serializer.is_valid():
                Line1= serializer.validated_data['contact_address_Line1']
                Line2= serializer.validated_data['contact_address_Line2']
                pin = serializer.validated_data['contact_address_PinCode']
                state = serializer.validated_data['contact_address_State']
                city = serializer.validated_data['contact_address_City']
                setattr(obj, 'contact_address_Line1', Line1)
                setattr(obj, 'contact_address_Line2', Line2)
                setattr(obj, 'contact_address_PinCode', pin)
                setattr(obj, 'contact_address_State', state)
                setattr(obj, 'contact_address_City', city)
                obj.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No account found'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        data = request.data
        user = request.user
        if BusinessDetail.objects.filter(company=user.company).exists():
            obj = BusinessDetail.objects.get(company=user.company)
            serializer=BusinessDetailSerializer(obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'No account found'}, status=status.HTTP_400_BAD_REQUEST)




