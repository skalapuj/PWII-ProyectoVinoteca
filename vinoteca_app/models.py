from django.db import models

class Contacto(models.Model):
    ASUNTOS_CHOICES = [
        ('consulta', 'Consulta General'),
        ('pedido', 'Pedido de Vinos'),
        ('visita', 'Reserva de Visita'),
    ]

    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=20, choices=ASUNTOS_CHOICES, default='consulta')
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta de {self.nombre} - {self.asunto}"