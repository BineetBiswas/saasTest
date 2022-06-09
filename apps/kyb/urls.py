from django.urls import path

from apps.kyb.apis import KybBankDetailView, KybBusinessDetailView, KybCinCheck, KybGstinCheck, KybProfile




urlpatterns = [
    path('profile/', KybProfile.as_view()),
    path('gstin-check/', KybGstinCheck.as_view()),
    path('cin-check/', KybCinCheck.as_view()),
    path('business-detail/', KybBusinessDetailView.as_view()),
    path('bank-detail/', KybBankDetailView.as_view()),

]