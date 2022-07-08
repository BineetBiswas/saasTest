from django.urls import path

from apps.sellers.apis import CustomerView, OrderView, ProductView, RBACView, TierView 


urlpatterns = [
    path('products/', ProductView.as_view()),
    path('tiers/', TierView.as_view()),
    path('tiers/<int:pk>', TierView.as_view()),
    path('customers/', CustomerView.as_view()),
    path('orders/', OrderView.as_view()),
    path('rbac/', RBACView.as_view()),
]