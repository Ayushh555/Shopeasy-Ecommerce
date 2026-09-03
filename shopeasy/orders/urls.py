from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/invoice/', views.order_invoice, name='order_invoice'),
    path('<int:order_id>/cancel/', views.order_cancel, name='order_cancel'),
]
