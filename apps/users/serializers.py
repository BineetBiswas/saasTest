from apps.users.models import User
from rest_framework import serializers
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'is_verified']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    

# class MyAuthTokenSerializer(serializers.Serializer):
#     email = serializers.EmailField(
#         label=("Email"),
#         write_only=True
#     )
#     otp = serializers.CharField(
#         label=("OTP"),
#         write_only=True
#     )
#     token = serializers.CharField(
#         label=("Token"),
#         read_only=True
#     )

#     def validate(self, attrs):
#         email = attrs.get('email')
#         otp = attrs.get('otp')

#         if email and otp:

#             validated_otp = User.objects.filter(email=email, otp=otp)
#             if not validated_otp:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = _('Must include "email" and "otp".')
#             raise serializers.ValidationError(msg, code='authorization')

#         # attrs['user'] = validated_otp.user
#         return attrs
