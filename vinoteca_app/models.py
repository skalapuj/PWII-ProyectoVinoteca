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

    categoria = models.CharField(max_length=50, editable=False, default='Consulta General')

    def save(self, *args, **kwargs):
        mensaje_minuscula = self.mensaje.lower()

        if any(palabra in mensaje_minuscula for palabra in ["precio", "costo", "tarifa", "compra"]):
            self.categoria = "Consulta Comercial"

        elif any(palabra in mensaje_minuscula for palabra in ["soporte", "error", "problema", "ayuda"]):
            self.categoria = "Consulta Técnica"

        elif any(palabra in mensaje_minuscula for palabra in ["trabajo", "cv", "empleo", "linkedin"]):
            self.categoria = "Consulta de RRHH"

        else:
            self.categoria = "Consulta General"

        super(Contacto, self).save(*args, **kwargs)

    def __str__(self):
        return f"Consulta de {self.nombre} - {self.categoria}"