from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Mesa, Reserva
from django.utils.timezone import now

# Página principal
def inicio(request):
    return render(request, 'reservas/inicio.html')

# Listar Clientes
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/clientes.html', {'clientes': clientes})

# Crear Cliente
def crear_cliente(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST['telefono']
        Cliente.objects.create(nombre=nombre, email=email, telefono=telefono)
        return redirect('listar_clientes')
    return render(request, 'clientes/crear_cliente.html')

# Editar Cliente
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.nombre = request.POST['nombre']
        cliente.email = request.POST['email']
        cliente.telefono = request.POST['telefono']
        cliente.save()
        return redirect('listar_clientes')
    return render(request, 'clientes/editar_cliente.html', {'cliente': cliente})

# Eliminar Cliente
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return redirect('listar_clientes')

# Listar Reservas
def listar_reservas(request):
    reservas = Reserva.objects.select_related('cliente', 'mesa').all()
    return render(request, 'reservas/listar_reservas.html', {'reservas': reservas})

# Crear Reserva
def crear_reserva(request):
    clientes = Cliente.objects.all()
    mesas = Mesa.objects.all()

    if request.method == 'POST':
        cliente_id = request.POST['cliente']
        mesa_id = request.POST['mesa']
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        personas = request.POST['personas']

        cliente = get_object_or_404(Cliente, id=cliente_id)
        mesa = get_object_or_404(Mesa, id=mesa_id)

        Reserva.objects.create(cliente=cliente, mesa=mesa, fecha=fecha, hora=hora, personas=personas)
        return redirect('listar_reservas')

    return render(request, 'reservas/crear_reserva.html', {'clientes': clientes, 'mesas': mesas})

# Eliminar Reserva
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.delete()
    return redirect('listar_reservas')
# Listar Mesas
def listar_mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'mesa/mesas.html', {'mesas': mesas})

# Crear Mesa
def crear_mesa(request):
    if request.method == 'POST':
        numero = request.POST['numero']
        capacidad = request.POST['capacidad']
        Mesa.objects.create(numero=numero, capacidad=capacidad)
        return redirect('listar_mesas')
    return render(request, 'mesa/crear_mesa.html')

# Editar Mesa
def editar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    if request.method == 'POST':
        mesa.numero = request.POST['numero']
        mesa.capacidad = request.POST['capacidad']
        mesa.save()
        return redirect('listar_mesas')
    return render(request, 'mesa/editar_mesa.html', {'mesa': mesa})

# Eliminar Mesa
def eliminar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    mesa.delete()
    return redirect('listar_mesas')