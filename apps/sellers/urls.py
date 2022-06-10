from django.urls import path

from apps.sellers.apis import ProductView 


urlpatterns = [
    path('products/', ProductView.as_view()),
]