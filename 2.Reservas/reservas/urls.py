from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    # Clientes
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),

    # Mesas
    path('mesas/', views.listar_mesas, name='listar_mesas'),
    path('mesas/nueva/', views.crear_mesa, name='crear_mesa'),
    path('mesas/editar/<int:mesa_id>/', views.editar_mesa, name='editar_mesa'),
    path('mesas/eliminar/<int:mesa_id>/', views.eliminar_mesa, name='eliminar_mesa'),

  # reservas
    path('reservas/', views.listar_reservas, name='listar_reservas'),
    path('reservas/nueva/', views.crear_reserva, name='crear_reserva'),
    path('reservas/eliminar/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
]
