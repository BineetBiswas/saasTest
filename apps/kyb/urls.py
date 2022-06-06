from django.urls import path

from apps.kyb.apis import KybProfile




urlpatterns = [
    path('profile/', KybProfile.as_view()),
    
]