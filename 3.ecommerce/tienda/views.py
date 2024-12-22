from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Producto, Carrito

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

import paypalrestsdk
from django.conf import settings

from .models import HistorialPago

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def reporte_pagos(request):
    pagos = HistorialPago.objects.all().order_by('-fecha')
    return render(request, 'pagos/reporte_pagos.html', {'pagos': pagos})

@login_required
def historial_pagos(request):
    pagos = HistorialPago.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'pagos/historial_pagos.html', {'pagos': pagos})


def procesar_pago(request):
    # Configuración de PayPal
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET,
    })

    # Obtener los productos del carrito
    carrito = Carrito.objects.all()
    total = sum(item.subtotal() for item in carrito)

    # Crear la transacción de PayPal
    pago = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://127.0.0.1:8000/pago-exitoso/",
            "cancel_url": "http://127.0.0.1:8000/pago-cancelado/",
        },
        "transactions": [{
            "item_list": {
                "items": [
                    {
                        "name": item.producto.nombre,
                        "price": f"{item.producto.precio}",
                        "currency": "USD",
                        "quantity": item.cantidad,
                    } for item in carrito
                ]
            },
            "amount": {"total": f"{total}", "currency": "USD"},
            "description": "Compra en Tienda Deportiva"
        }]
    })

    if pago.create():
        # Registrar pago en el historial como pendiente
        HistorialPago.objects.create(
            usuario=request.user,
            total=total,
            estado="Pendiente",
            detalles=pago.id  # Almacenar el ID de transacción de PayPal
        )

        for link in pago.links:
            if link.method == "REDIRECT":
                return redirect(link.href)
    else:
        # Registrar pago fallido
        HistorialPago.objects.create(
            usuario=request.user,
            total=total,
            estado="Error",
            detalles=str(pago.error)
        )
        return render(request, 'pagos/pago_error.html', {"error": pago.error})

def pago_exitoso(request):
    # Limpiar el carrito después de un pago exitoso
    Carrito.objects.all().delete()
    return render(request, 'pagos/pago_exitoso.html')

def pago_cancelado(request):
    return render(request, 'pagos/pago_cancelado.html')

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Asignar rol de cliente por defecto
            cliente_group = Group.objects.get(name='Clientes')
            user.groups.add(cliente_group)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})
@login_required
def perfil_usuario(request):
    return render(request, 'usuarios/perfil_usuario.html', {'usuario': request.user})

# Listar Categorías
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/categorias.html', {'categorias': categorias})

# Crear Categoría
def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        Categoria.objects.create(nombre=nombre, descripcion=descripcion)
        return redirect('listar_categorias')
    return render(request, 'categorias/crear_categoria.html')

# Editar Categoría
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        categoria.nombre = request.POST['nombre']
        categoria.descripcion = request.POST['descripcion']
        categoria.save()
        return redirect('listar_categorias')
    return render(request, 'categorias/editar_categoria.html', {'categoria': categoria})

# Eliminar Categoría
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    return redirect('listar_categorias')

# Filtrar Productos por Categoría
def filtrar_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'productos/listar_productos.html', {'productos': productos, 'categoria': categoria})
from django.contrib.auth.decorators import user_passes_test

def es_administrador(user):
    return user.groups.filter(name='Administradores').exists()

# @user_passes_test(es_administrador)
def crear_producto(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']
        categoria_id = request.POST['categoria']
        stock = request.POST['stock']
        imagen = request.FILES.get('imagen')

        categoria = get_object_or_404(Categoria, id=categoria_id)
        Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            categoria=categoria,
            stock=stock,
            imagen=imagen
        )
        return redirect('listar_productos')

    return render(request, 'productos/crear_producto.html', {'categorias': categorias})


def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST['descripcion']
        producto.precio = request.POST['precio']
        producto.categoria = get_object_or_404(Categoria, id=request.POST['categoria'])
        producto.stock = request.POST['stock']

        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']

        producto.save()
        return redirect('listar_productos')

    return render(request, 'productos/editar_producto.html', {
        'producto': producto,
        'categorias': categorias,
    })
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('listar_productos')

# Lista de productos por categoría
def listar_productos(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    filtro_categoria = request.GET.get('categoria', '')

    if filtro_categoria:
        productos = productos.filter(categoria__id=filtro_categoria)

    return render(request, 'productos/listar_productos.html', {
        'productos': productos,
        'categorias': categorias,
        'filtro_categoria': filtro_categoria,
    })


# Detalle de un producto
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})


# @login_required
# Ver carrito
def ver_carrito(request):
    carrito = Carrito.objects.all()
    total = sum(item.subtotal() for item in carrito)

    # Filtro por nombre del producto
    filtro = request.GET.get('filtro', '')
    if filtro:
        carrito = carrito.filter(producto__nombre__icontains=filtro)

    return render(request, 'carrito/carrito.html', {'carrito': carrito, 'total': total, 'filtro': filtro})

# Agregar producto al carrito
def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    item, created = Carrito.objects.get_or_create(producto=producto)
    if not created:
        item.cantidad += 1
    item.save()
    return redirect('ver_carrito')

# Eliminar producto del carrito
def eliminar_carrito(request, item_id):
    item = get_object_or_404(Carrito, id=item_id)
    item.delete()
    return redirect('ver_carrito')


