from django.shortcuts import render
from apps.users.serializers import LoginSerializer, UserSerializer, VerifyAccountSerializer
from apps.users.utils import send_otp_via_email
from apps.users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import status
import pyotp

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['company'] = user.company.company_name
    refresh['kyc_required']=user.kyc_required
    refresh['is_kyc_done']=user.company.is_kyc_done
    refresh['is_kyb_done']=user.company.is_kyb_done

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class RegisterAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data = data)
            if serializer.is_valid():
            
                
                serializer.save()
                send_otp_via_email(serializer.data['email'])
                return Response({
                    'status': 200,
                    'message': "Check email",
                    'data': serializer.data
                })
            

            return Response({
                'status': 400,
                'message': "something went wrong",
                'data': serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': "something went wrong",
                
            })


class LoginAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                if User.objects.filter(email=serializer.data['email']).exists():
                    send_otp_via_email(serializer.data['email'])
                    return Response({
                        'status': 200,
                        'message': "Check email",
                        'data': serializer.data
                    })
                
                return Response({
                        'status': 400,
                        'message': "This email does not exist",
                        'data': "No records found"
                    })

            return Response({
                'status': 400,
                'message': "something went wrong",
                'data': serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': "something went wrong",
                
            })


# class VerifyOTP(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         try:
#             data = request.data
#             serializer = VerifyAccountSerializer(data = data)
#             if serializer.is_valid():
#                 email = serializer.data['email']
#                 otp = serializer.data['otp']

#                 user = User.objects.filter(email = email)
#                 if not user.exists():
#                     return Response({
#                     'status': 400,
#                     'message': "something went wrong",
#                     'data': 'invalid email'
#                 })

#                 if not user[0].otp == otp:
#                     return Response({
#                     'status': 400,
#                     'message': "something went wrong",
#                     'data': 'invalid otp'
#                 })

#                 user = user.first()
#                 user.is_verified = True
#                 user.set_password(otp)
#                 setattr(user, 'username', email)
#                 print(user.username, user.password)
#                 user.save()

                
#                 return Response({
#                     'status': 200,
#                     'message': "Account Verified",
#                     'data': get_tokens_for_user(user)
#                 })

#             return Response({
#                 'status': 400,
#                 'message': "something went wrong",
#                 'data': serializer.errors
#             })
#         except Exception as e:
#             print(e)


class VerifyOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data = data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                otp = serializer.validated_data['otp']
                

                user = User.objects.filter(email = email)
                if not user.exists():
                    return Response({
                    'status': 400,
                    'message': "something went wrong",
                    'data': 'invalid email'
                })


                if not user[0].otp == otp:
                    return Response({
                    'status': 400,
                    'message': "something went wrong",
                    'data': 'invalid otp'
                })
                else:

                    user = user.first()
                    activation_key = user.activation_key
                    totp = pyotp.TOTP(activation_key, interval=120)
                    verify = totp.verify(otp)

                    if verify:
                        user.is_verified = True
                        user.save()
                        print(user.company.admin_id)
                    
                        return Response({
                            'status': 200,
                            'message': "Account Verified",
                            'data': get_tokens_for_user(user)
                        })

                    else:
                        return Response({"Time out" : "Given otp is expired!!"}, status=status.HTTP_408_REQUEST_TIMEOUT)

            return Response({
                'status': 400,
                'message': "something went wrong",
                'data': serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({"No User" : "Invalid otp OR No active user found for given otp"}, status=status.HTTP_400_BAD_REQUEST)



class ResendOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                

                user = User.objects.filter(email = email)
                if not user.exists():
                    return Response({
                    'status': 400,
                    'message': "something went wrong",
                    'data': 'invalid email'
                })

                result, time = send_otp_via_email(email)

                if result:
                    return Response({
                            'status': 200,
                            'message': "New otp sent to your email",
                            'data': serializer.data
                        })
                else:
                    return Response({
                        'status': 400,
                        'error': f"Please try after {time} seconds",
                        
                    })

            return Response({
                'status': 400,
                'message': "something went wrong",
                'data': serializer.errors
            })
            
        
        except Exception as e:
            print(e)