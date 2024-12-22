from django.contrib import admin
from .models import Cliente, Membresia, Pago

admin.site.register(Cliente)
admin.site.register(Membresia)
admin.site.register(Pago)