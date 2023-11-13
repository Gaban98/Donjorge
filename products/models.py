from django.db import models
from users.models import Users
from users.models import Users

# Create your models here.

class Category(models.Model):
    description = models.CharField(max_length=50)
    

    def __str__(self):
        return self.description
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

class Product(models.Model):
    name = models.CharField(max_length=100, null=False)
    description_product = models.CharField(max_length=300, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=10, null=False)
    stock = models.IntegerField(null=True)
    imgBig = models.ImageField(upload_to='productos', null=True)
    imgSmall = models.ImageField(upload_to='iconos', null=True)
    category_product = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class Cars(models.Model):
    STATE_PRO = {
        ('Activo', 'Activo'),
        ('Comprado', 'Comprado'),
        ('Anulado', 'Anulado'),
    }
    
    cars_user = models.ForeignKey(Users, on_delete=models.CASCADE, null=False)
    product_cars = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    amount = models.IntegerField(null=False, default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    state = models.CharField(max_length=100, choices=STATE_PRO, default='activo')
    


    def __str__(self):
        return f"{self.amount} x {self.product_cars.name}"

    
    class Meta:
        verbose_name = 'Carro'
        verbose_name_plural = 'Carros'