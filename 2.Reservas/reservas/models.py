from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField()  # Número máximo de personas

    def __str__(self):
        return f"Mesa {self.numero} - Capacidad: {self.capacidad}"


class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    personas = models.IntegerField()

    def __str__(self):
        return f"{self.cliente.nombre} - {self.fecha} {self.hora}"
