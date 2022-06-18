from django.urls import path


from apps.users.apis import LoginAPI, RegisterAPI, ResendOTP, VerifyOTP
from rest_framework_simplejwt.views import (TokenRefreshView,
)




urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('verify/', VerifyOTP.as_view()),
    path('resend-otp/', ResendOTP.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
]