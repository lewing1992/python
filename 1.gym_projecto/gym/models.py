from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Membresia(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)  # Ejemplo: Mensual, Anual
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"{self.cliente.nombre} - {self.tipo}"

class Pago(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_pago = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.cliente.nombre} - {self.monto}"
