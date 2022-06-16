from django.urls import path


from apps.users.apis import LoginAPI, RegisterAPI, ResendOTP, VerifyOTP
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
)




urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('verify/', VerifyOTP.as_view()),
    path('resend-otp/', ResendOTP.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/', MyObtainAuthToken.as_view(), name='token_obtain_pair'),
    # path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
]