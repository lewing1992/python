from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.conf import settings
from django.contrib.staticfiles.urls import static
urlpatterns = [


    path('historial-pagos/', views.historial_pagos, name='historial_pagos'),
    path('reporte-pagos/', views.reporte_pagos, name='reporte_pagos'),


    path('procesar-pago/', views.procesar_pago, name='procesar_pago'),
    path('pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago-cancelado/', views.pago_cancelado, name='pago_cancelado'),

    # Login y Logout
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Registro y Perfil
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    
    # Productos y Carrito
    path('', views.listar_productos, name='listar_productos'),

    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

   path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_carrito, name='eliminar_carrito'),

    # Categorías
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('productos/categoria/<int:categoria_id>/', views.filtrar_por_categoria, name='filtrar_por_categoria'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

