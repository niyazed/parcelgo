from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),

    path('ddash', views.ddash, name='delivery_dash'),

    path('cdash', views.cdash, name='customer_dash'),
    path('ongoing-order', views.ongoing_order, name='ongoing-order'),
    path('order-history', views.order_history, name='order-history'),
]