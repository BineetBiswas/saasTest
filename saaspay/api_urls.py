from django.urls import path, include

urlpatterns = [
    path('kyb/', include('apps.kyb.urls')),
    path('users/', include('apps.users.urls')),
    
]