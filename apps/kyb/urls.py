from django.urls import path

from apps.kyb.apis import KybCinCheck, KybGstinCheck, KybProfile




urlpatterns = [
    path('profile/', KybProfile.as_view()),
    path('gstin-check/', KybGstinCheck.as_view()),
    path('cin-check/', KybCinCheck.as_view()),
]