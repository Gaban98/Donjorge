from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'description',]
admin.site.register(Category, CategoryAdmin)

#--------------------------------------------------------------

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description_product', 'stock',]
admin.site.register(Product, ProductAdmin)

#--------------------------------------------------------------

class CarsAdmin(admin.ModelAdmin):
    list_display = ['cars_user', 'product_cars', 'amount', 'state',]
admin.site.register(Cars, CarsAdmin)