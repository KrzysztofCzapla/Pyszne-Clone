from django.contrib import admin

from .models import Restaurant,FoodItem,RestaurantReview,Order,Cart,FoodPackage

admin.site.register(Restaurant)
admin.site.register(FoodItem)
admin.site.register(RestaurantReview)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(FoodPackage)