from django.shortcuts import render, redirect
from .models import *
from users.models import Users
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse

from .forms import *
from django.conf import settings

import json
from django.http import JsonResponse, HttpResponse
import os
from django import template
from io import BytesIO

#import qrcode



# Create your views here.


def ViewCategory(request):
    ListCategory = Category.objects.all()
    context = {'categorias': ListCategory, 'titulo': 
            'Categorias de los productos '}
    return render(request, 'products/category.html', context)

#-----------------PRODUCTOS-----------------

def ViewProductCategory(request, idCategory):
    NameCategory = Category.objects.get(id=idCategory)
    ListProduct = Product.objects.filter(category_product=idCategory)
    context = {'productos': ListProduct, 'titulo': 
            'Productos de la categoria: ' + NameCategory.description}
    return render(request, 'products/view_products.html', context)

def ViewProduct (request, idProduct, msj = None):
    ViewProducts = Product.objects.get(id=idProduct)
    context = {'producto': ViewProducts, 
            'titulo': 'Detalles del producto: ' + str(ViewProducts.description_product)}
    if msj:
        context['mensaje'] = msj
    return render(request, 'products/product_unity.html', context)

def ViewsAllProducts (request):
    #consultar las categorias
    ListCategory = Category.objects.all().values('id', 'description')
    #consultar los productos
    ListProduct = Product.objects.all().values('id', 'name', 'category_product')
    #renderizar la vista
    context = {
        'Categoria': ListCategory,
        'Productos': ListProduct,
        'titulo': 'Todos los productos'}
    
    return render(request, 'products/viewall.html', context)

#-----------------CARRITO-----------------
@login_required
def AddShoppingCar(request, idProduct):
    RegUser = request.user
    msj = None
    # leer registro del producto en el carro
    Existence = Product.objects.filter(id=idProduct).exists()
    if Existence:
        ProductCar = Product.objects.get(id=idProduct)
        # si no existe en el carrito
        Existence = Cars.objects.filter(product_cars=ProductCar, state= 'activo', cars_user=RegUser).exists()
        if Existence:
            # instancia un objeto de la clase del carrito
            Addcar = Cars(product_cars=ProductCar, state='activo', cars_user=RegUser, price=ProductCar.price, amount=1)
            # incrementa la cantidad del producto
            Addcar.amount += 1
            Addcar.save()
        else:
            Addcar = Cars(product_cars=ProductCar, state='activo', cars_user=RegUser, price=ProductCar.price)
            Addcar.save()
        msj = 'Producto agregado al carrito'
    else:
        msj = 'El producto no existe'
    # redirecciona a la vista del producto
    return ViewProduct(request, idProduct, msj)


def ShoppingCarView(request):
    context = ConsultCar(request)
    return render(request, 'products/shopping_car.html', context)


def DeleteProductCar(request, idProduct):
    # consultar el reg y cambiar el estado a inactivo
    RegCar = Cars.objects.get(id=idProduct)
    RegCar.state = 'anulado'
    # guardar el registro
    RegCar.save()
    #redireccionar a la vista del carro
    return ShoppingCarView(request)


def ChangeProductCar(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            #toma la data enviada por el cliente
            data = json.load(request)
            id = data.get('id')
            cantidad = int(data.get('cantidad'))
            if cantidad > 0:
                #consultar el reg y cambiar la cantidad
                if Cars.objects.filter(id=id).exists():
                    RegCar = Cars.objects.get(id=id)
                    RegCar.amount = cantidad
                    #guardar el registro
                    RegCar.save()
            context = ConsultCar(request)    
            #retornar la respuesta en formato JSON
            return JsonResponse(context)
        return JsonResponse({'error': 'No se pudo procesar la solicitud'}, status=400)    
    else:
        return ShoppingCarView(request)
    
def ConsultCar(request):
    RegUser = request.user
    # leer registro del producto en el carro
    lista_productos = Cars.objects.filter(cars_user=RegUser, state='activo').values(
    'id',
    'price',
    'amount',
    'product_cars__name',
    'product_cars__imgSmall',
    'product_cars__id',
    'product_cars__unit')

    # renderizar la vista
    listado = []
    subtotal = 0
    for producto in lista_productos:
        reg = {
            'id': producto['id'],
            'cantidad': producto['amount'],
            'precio': producto['price'],
            'imagen': producto['product_cars__imgSmall'],
            'nombre': producto['product_cars__name'],
            'unidad': producto['product_cars__unit'],
            'total': producto['amount'] * producto['price'],
            'id_producto': producto['product_cars__id'],
        }
        subtotal += producto['amount'] * producto['price']
        listado.append(reg)
    envio = 8000
    if len(listado) == 0:
        envio = 0

    context = {
        'titulo': 'Productos en el carrito de compras',
        'listado': listado,
        'subtotal': subtotal,
        'iva': int(subtotal) * 0.19,
        'envio': envio,
        'total': (int(subtotal) * 1.19) + envio
    }
    return context
    

def AllProductsCategory(request):
    categories = Category.objects.all().order_by('description')
    products = Product.objects.all().order_by('name', 'description_product')
    context = {
        'categories': categories,
        'products': products,
        'titulo': 'Productos por categoría',
        'os': os,
    }
    return render(request, 'products/ViewProductForCategory.html', context)

#-----------------PEDIDOS POR CORREO-----------------

def Pay(request):
    context = ConsultCar(request)
    RegUser = request.user
    NameUser = str(RegUser.first_name) + ' ' + str(RegUser.last_name)
    context['nameUser'] = NameUser    
    email = RegUser.email

    #enviar el correo
    mail_subject = 'Pedido de compra'

    body = render_to_string('products/email.html', context=context)
    to_email = [email] #email del usuario lista los correos

    send_email = EmailMessage(mail_subject, body, to=to_email)
    send_email.content_subtype = 'html'
    send_email.send()

    #fin de modulo de enviar correo

    #sacar productos del carrito
    ListCar = Cars.objects.filter( cars_user=RegUser, state='activo' )
    for car in ListCar:
        car.state = 'Comprado'
        car.save()

    #redireccionar a la vista del carro
    return ShoppingCarView(request)

# -------------------- para crear con QR --------------------|