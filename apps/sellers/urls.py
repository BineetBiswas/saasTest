from django.urls import path

from apps.sellers.apis import ProductView, TierView 


urlpatterns = [
    path('products/', ProductView.as_view()),
    path('tiers/', TierView.as_view()),
    path('tiers/<int:pk>', TierView.as_view()),
]