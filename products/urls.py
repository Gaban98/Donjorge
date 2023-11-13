from django.urls import path
from . import views
from shop.views import home


urlpatterns = [
    path('', home, name='home'),

    path('category/', views.ViewCategory, name='ViewCategory'),

    path('products/<int:idCategory>', views.ViewProductCategory, name='ViewProductCategory'),
    path('product/<int:idProduct>', views.ViewProduct, name='ViewProduct'),

    path('ViewsAllProducts/', views.ViewsAllProducts, name='ViewsAllProducts'),
    
    path('AddShoppingCar/<int:idProduct>', views.AddShoppingCar, name='AddShoppingCar'),
    path('ShoppingCarView/', views.ShoppingCarView, name='ShoppingCarView'),
    path('DeleteProductCar/<int:idProduct>', views.DeleteProductCar, name='DeleteProductCar'),
    path('ChangeProductCar/', views.ChangeProductCar, name='ChangeProductCar'),
    path('AllProductsCategory/', views.AllProductsCategory, name='AllProductsCategory'),

    path('Pay/', views.Pay, name='Pay'),

]