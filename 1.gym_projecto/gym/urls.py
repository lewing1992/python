from django.urls import path
from . import views

urlpatterns = [
    # Clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    
    # Membresías
    path('membresias/', views.lista_membresias, name='lista_membresias'),
    path('membresias/nueva/', views.crear_membresia, name='crear_membresia'),
    path('membresias/editar/<int:membresia_id>/', views.editar_membresia, name='editar_membresia'),
    path('membresias/eliminar/<int:membresia_id>/', views.eliminar_membresia, name='eliminar_membresia'),
    
    # Pagos
    path('pagos/', views.lista_pagos, name='lista_pagos'),
    path('pagos/nuevo/', views.crear_pago, name='crear_pago'),
    path('pagos/eliminar/<int:pago_id>/', views.eliminar_pago, name='eliminar_pago'),
    #DASH
    path('dashboard/', views.dashboard, name='dashboard'),
]
