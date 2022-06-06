from django.urls import path


from apps.users.apis import LoginAPI, RegisterAPI, VerifyOTP




urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('verify/', VerifyOTP.as_view()),
    # path('token/', MyObtainAuthToken.as_view(), name='token_obtain_pair'),
    # path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
]