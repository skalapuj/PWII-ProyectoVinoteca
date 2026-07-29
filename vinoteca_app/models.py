from django.db import models
from django.contrib.auth.models import User

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

class UsuarioPermitido(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, default="")
    email = models.EmailField(unique=True)
    codigo_validation = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.email} ({self.nombre})"

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_shared_with_user:=models.CASCADE)
    cuenta_validada = models.BooleanField(default=False)

    def __str__(self):
        return f"Perfil de {self.user.username} - Validado: {self.cuenta_validada}"

class ContenidoNosotros(models.Model):
    # Sección 1: Nuestra Historia
    titulo_historia = models.CharField(
        max_length=200, 
        default="Nuestra Historia", 
        verbose_name="Título Historia"
    )
    parrafo1_historia = models.TextField(
        verbose_name="Historia - Párrafo 1",
        default="Fundada en el corazón del Valle de Uco, nuestra bodega nació de un sueño familiar: transformar la pureza del agua de montaña y la fuerza del sol mendocino en vinos con alma."
    )
    parrafo2_historia = models.TextField(
        verbose_name="Historia - Párrafo 2",
        default="Desde hace tres generaciones, mantenemos el compromiso de intervenir lo menos posible en el proceso natural, permitiendo que cada botella sea un reflejo fiel de su terruño."
    )

    # Sección 2: El Secreto
    titulo_secreto = models.CharField(
        max_length=200, 
        default="El Secreto", 
        verbose_name="Título El Secreto"
    )
    parrafo1_secreto = models.TextField(
        verbose_name="El Secreto - Párrafo 1",
        default="Creemos que el vino se hace en el viñedo. Por eso, cuidamos nuestras vides con técnicas orgánicas y una cosecha manual que respeta los tiempos de la naturaleza."
    )
    parrafo2_secreto = models.TextField(
        verbose_name="El Secreto - Párrafo 2",
        default="La altitud y la amplitud térmica de nuestra zona nos brindan uvas de una concentración y frescura excepcionales, que luego descansan en barricas de roble francés."
    )

    ultima_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contenido de Nosotros"
        verbose_name_plural = "Contenido de Nosotros"

    def __str__(self):
        return f"Contenido de Nosotros (Última edición: {self.ultima_modificacion.strftime('%d/%m/%Y %H:%M')})"