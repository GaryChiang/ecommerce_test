from django.contrib import admin
from ecommerce.models import ProductType, Product, Customer, Restaurant, OrderMaster, OrderDetail, Category, DeliveryStaff

# Register your models here.
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(OrderMaster)
admin.site.register(OrderDetail)
admin.site.register(Category)
admin.site.register(DeliveryStaff)
