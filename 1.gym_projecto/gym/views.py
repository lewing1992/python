from django.utils.timezone import now
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Membresia, Pago

# Lista de Clientes
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/clientes.html', {'clientes': clientes})

# Crear Cliente
def crear_cliente(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST['telefono']
        Cliente.objects.create(nombre=nombre, email=email, telefono=telefono)
        return redirect('lista_clientes')
    return render(request, 'clientes/crear_cliente.html')

# Editar Cliente
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.email = request.POST['email']
        cliente.telefono = request.POST['telefono']
        cliente.save()
        return redirect('lista_clientes')
    return render(request, 'clientes/editar_cliente.html', {'cliente': cliente})

# Eliminar Cliente
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('lista_clientes')

# Lista de Membresías
def lista_membresias(request):
    membresias = Membresia.objects.select_related('cliente').all()
    return render(request, 'membresias/membresias.html', {'membresias': membresias})

# Crear Membresía
def crear_membresia(request):
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        cliente_id = request.POST['cliente']
        tipo = request.POST['tipo']
        precio = request.POST['precio']
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        cliente = get_object_or_404(Cliente, id=cliente_id)
        Membresia.objects.create(
            cliente=cliente, tipo=tipo, precio=precio,
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
        )
        return redirect('lista_membresias')
    return render(request, 'membresias/crear_membresia.html', {'clientes': clientes})

# Editar Membresía
def editar_membresia(request, membresia_id):
    membresia = get_object_or_404(Membresia, id=membresia_id)
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        membresia.cliente_id = request.POST['cliente']
        membresia.tipo = request.POST['tipo']
        membresia.precio = request.POST['precio']
        membresia.fecha_inicio = request.POST['fecha_inicio']
        membresia.fecha_fin = request.POST['fecha_fin']
        membresia.save()
        return redirect('lista_membresias')
    return render(request, 'membresias/crear_membresia.html', {'membresia': membresia, 'clientes': clientes})

# Eliminar Membresía
def eliminar_membresia(request, membresia_id):
    membresia = get_object_or_404(Membresia, id=membresia_id)
    membresia.delete()
    return redirect('lista_membresias')
# Lista de Pagos
def lista_pagos(request):
    pagos = Pago.objects.select_related('cliente').all()
    return render(request, 'pagos/pagos.html', {'pagos': pagos})

# Crear Pago
def crear_pago(request):
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        cliente_id = request.POST['cliente']
        monto = request.POST['monto']
        cliente = get_object_or_404(Cliente, id=cliente_id)
        Pago.objects.create(cliente=cliente, monto=monto)
        return redirect('lista_pagos')
    return render(request, 'pagos/crear_pago.html', {'clientes': clientes})

# Eliminar Pago
def eliminar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    pago.delete()
    return redirect('lista_pagos')
# Dashboard
def dashboard(request):
    # Total de clientes
    total_clientes = Cliente.objects.count()
    
    # Membresías vigentes
    membresias_vigentes = Membresia.objects.filter(fecha_fin__gte=now().date()).count()
    
    # Total de pagos registrados y monto total
    total_pagos = Pago.objects.count()
    monto_total_pagos = Pago.objects.aggregate(total=Sum('monto'))['total'] or 0

    context = {
        'total_clientes': total_clientes,
        'membresias_vigentes': membresias_vigentes,
        'total_pagos': total_pagos,
        'monto_total_pagos': monto_total_pagos,
    }
    return render(request, 'dashboard/dash.html', context)
