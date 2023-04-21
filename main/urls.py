from django.urls import path

from . import views
app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('<SearchType>/', views.index, name='index'),
    path('profile/<userID>/', views.profile, name='profile'),
    path('success/success/', views.orderdone, name='orderdone'),
    path('Restaurant/<RestaurantName>/', views.restaurantDetails, name='restaurantDetails'),
    path('Restaurant/<RestaurantName>/Reviews', views.restaurantReviews, name='restaurantReviews'),
    path('Restaurant/<RestaurantName>/Order', views.order, name='order'),
    path('cart/addToCart/', views.addToCart, name='addToCart'),
    path('cart/deleteFromCart/', views.deleteFromCart, name='deleteFromCart'),
    path('api/orders/', views.order_collection, name = 'order_collection'),
    path('api/order/<orderID>/', views.order_element, name = 'order_element'),
    path('api/orders/add/', views.AddOrderAPI, name = 'AddOrderAPI'), 
]