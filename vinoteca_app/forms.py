from django import forms
from django.core.validators import EmailValidator

class ContactoForm(forms.Form):
    # ==========================================
    # 1. DATOS PERSONALES
    # ==========================================
    nombre = forms.CharField(
        max_length=100,
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'nombre',
            'placeholder': 'Tu nombre...'
        }),
        error_messages={
            'required': 'El nombre completo es obligatorio.',
            'min_length': 'El nombre debe tener al menos 3 caracteres.',
            'max_length': 'El nombre es demasiado largo.'
        }
    )

    email = forms.EmailField(
        required=True,
        validators=[EmailValidator(message="El formato del correo electrónico no es válido.")],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': 'email@ejemplo.com'
        }),
        error_messages={
            'required': 'El correo electrónico es obligatorio.'
        }
    )

    # ==========================================
    # 2. DETALLES DE LA CONSULTA
    # ==========================================
    OPCIONES_ASUNTOS = [
        ('consulta', 'Consulta General'),
        ('pedido', 'Pedido de Vinos'),
        ('visita', 'Reserva de Visita'),
    ]

    asunto = forms.ChoiceField(
        choices=OPCIONES_ASUNTOS,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'asunto'
        }),
        error_messages={
            'required': 'Debe seleccionar un asunto de la lista.'
        }
    )

    mensaje = forms.CharField(
        required=True,
        min_length=10,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'mensaje',
            'rows': 5,
            'placeholder': '¿En qué podemos ayudarte?'
        }),
        error_messages={
            'required': 'El mensaje de la consulta es obligatorio.',
            'min_length': 'El mensaje debe tener al menos 10 caracteres.'
        }
    )