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


class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    apellido = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Cree su contraseña segura'}))

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(char.isupper() for char in password):
            raise ValidationError("La contraseña debe incluir al menos una letra mayúscula.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("La contraseña debe incluir al menos un número.")

        return password

class ValidacionCodigoForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}))
    codigo = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresá el código enviado'}))

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Tu contraseña'}))