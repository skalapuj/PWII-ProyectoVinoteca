from .forms import ContactoForm, RegistroForm, ValidacionCodigoForm, LoginForm
from .models import Contacto, UsuarioPermitido, PerfilUsuario
from .serializers import VinoExternoSerializer
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
from django.views import View

def home(request):
    return render(request, 'vinoteca_app/index.html')

def nosotros(request):
    return render(request, 'vinoteca_app/nosotros.html')

def contacto(request):
    if request.method == 'GET':
        form = ContactoForm()
        return render(request, 'vinoteca_app/contacto.html', {'form': form})

    elif request.method == 'POST':
        form = ContactoForm(request.POST)

        if form.is_valid():
            datos_limpios = form.cleaned_data
            try:
                nueva_consulta = Contacto.objects.create(
                    nombre=datos_limpios['nombre'],
                    email=datos_limpios['email'],
                    asunto=datos_limpios['asunto'],
                    mensaje=datos_limpios['mensaje']
                )
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'errors': [f"Error crítico al guardar en Base de Datos: {str(e)}"]
                }, status=500)

            try:
                asunto_mail = f"Confirmación de Consulta - Vinoteca Reserva"

                asunto_legible = dict(ContactoForm.OPCIONES_ASUNTOS).get(datos_limpios['asunto'], 'Consulta')

                cuerpo_mensaje = (
                    f"Hola {datos_limpios['nombre']},\n\n"
                    f"¡Gracias por comunicarte con Vinoteca Reserva!\n"
                    f"Hemos recibido tu mensaje de forma exitosa en nuestro sistema.\n\n"
                    f"Detalle de tu solicitud:\n"
                    f"==================================================\n"
                    f"• Tipo de Trámite: {asunto_legible}\n"
                    f"• Tu Correo: {datos_limpios['email']}\n"
                    f"• Mensaje enviado: \"{datos_limpios['mensaje']}\"\n"
                    f"==================================================\n\n"
                    f"Un sommelier o asesor comercial se estará comunicando con vos a la brevedad "
                    f"para responder tu consulta de forma personalizada.\n\n"
                    f"Atentamente,\n"
                    f"El equipo de Vinoteca Reserva S.A. 2026."
                )

                # send_mail(
                #     subject=asunto_mail,
                #     message=cuerpo_mensaje,
                #     from_email=settings.DEFAULT_FROM_EMAIL,
                #     recipient_list=[datos_limpios['email']],
                #     fail_silently=False,
                # )
                print(f"Correo de confirmación enviado con éxito a: {datos_limpios['email']}")

            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'errors': [f"Error crítico al enviar el email: {str(e)}"]
                }, status=500)

            return JsonResponse({
                'status': 'success',
                'message': '¡Tu consulta fue procesada y guardada con éxito!'
            })

        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Método no permitido'
    }, status=405)

def registro_view(request):
    if request.method == 'GET':
        form = RegistroForm()
        return render(request, 'vinoteca_app/auth/registro.html', {'form': form})

    elif request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            email_ingresado = form.cleaned_data['email']

            user_existente = User.objects.filter(email=email_ingresado).first()
            if user_existente:
                perfil = PerfilUsuario.objects.filter(user=user_existente).first()
                if perfil and perfil.cuenta_validada:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Este correo ya se encuentra registrado y validado. Inicie sesión.'
                    }, status=400)
                else:
                    permitido = UsuarioPermitido.objects.filter(email=email_ingresado).first()
                    if permitido:
                        request.session['email_a_validar'] = email_ingresado
                        send_mail(
                            subject="Validación de Cuenta - Reenvío de Código",
                            message=f"Hola {permitido.nombre},\n\nTu cuenta ya está pre-registrada pero le falta validación.\nCódigo: {permitido.codigo_validation}",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[email_ingresado],
                            fail_silently=False,
                        )
                        return JsonResponse({
                            'status': 'success',
                            'message': 'La cuenta ya existe pero falta validar. Le reenviamos el correo.'
                        })

            permitido = UsuarioPermitido.objects.filter(email=email_ingresado).first()

            if permitido:
                username = email_ingresado.split('@')[0]
                user = User.objects.create_user(
                    username=username,
                    email=email_ingresado,
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['nombre'],
                    last_name=form.cleaned_data['apellido']
                )

                user.is_staff = True
                user.is_superuser = True
                user.save()

                PerfilUsuario.objects.create(user=user, cuenta_validada=False)

                try:
                    asunto_auth = "Validación de Cuenta - Panel de Administración Vinoteca Reserva"

                    cuerpo_auth = (
                        f"Hola {permitido.nombre},\n\n"
                        f"Se ha iniciado un pedido de registro para tu cuenta en el Panel de Administración de Vinoteca Reserva.\n"
                        f"Como el acceso es restringido, necesitamos que verifiques tu identidad ingresando el código de seguridad obligatorio.\n\n"
                        f"Tus datos de acceso para verificar:\n"
                        f"==================================================\n"
                        f"• Código de Validación: {permitido.codigo_validation}\n"
                        f"• Enlace de Verificación: http://127.0.0.1:8000/validar-cuenta/\n"
                        f"==================================================\n\n"
                        f"Copia el código anterior, ingresa al enlace provisto y pégalo para habilitar tu cuenta en el sistema.\n\n"
                        f"Si no solicitaste este acceso, por favor desestima este correo.\n\n"
                        f"Saludos cordiales,\n"
                        f"Soporte Técnico - Vinoteca Reserva S.A. 2026."
                    )

                    send_mail(
                        subject=asunto_auth,
                        message=cuerpo_auth,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email_ingresado],
                        fail_silently=False,
                    )

                    print(f"Código de validación enviado por correo a: {email_ingresado}")

                    request.session['email_a_validar'] = email_ingresado

                    return JsonResponse({
                        'status': 'success',
                        'message': 'Le llegará un correo para validar su cuenta.'
                    })

                except Exception as e:
                    return JsonResponse({
                        'status': 'error',
                        'errors': [f"Error crítico al enviar en email: {str(e)}"]
                    }, status=500)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Acceso restringido. No está autorizado a utilizar este sistema.'
                }, status=403)

        else:
            errores = []
            for campo, lista_errores in form.errors.items():
                for err in lista_errores:
                    errores.append(f"{err}")
            msg_error = " y ".join(errores)

            return JsonResponse({
                'status': 'error',
                'message': msg_error
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def validar_cuenta_view(request):
    email_session = request.session.get('email_a_validar', '')
    if request.method == 'POST':
        form = ValidacionCodigoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            codigo_ingresado = form.cleaned_data['codigo']

            permitido = UsuarioPermitido.objects.filter(email=email, codigo_validation=codigo_ingresado).first()

            if permitido:
                user = User.objects.get(email=email)
                perfil = PerfilUsuario.objects.get(user=user)
                perfil.cuenta_validada = True
                perfil.save()

                messages.success(request, "¡Cuenta validada con éxito! Ya podés iniciar sesión.")
                return redirect('login')
            else:
                messages.error(request, "El código de validación ingresado es incorrecto.")
    else:
        form = ValidacionCodigoForm(initial={'email': email_session})
    return render(request, 'vinoteca_app/auth/validar.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user_obj = User.objects.filter(email=email).first()

            if user_obj:
                perfil = PerfilUsuario.objects.filter(user=user_obj).first()
                if perfil and not perfil.cuenta_validada:
                    messages.error(request, "Esta cuenta aún no ha sido validada por correo.")
                    request.session['email_a_validar'] = email
                    return redirect('validar_cuenta')

                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('admin:index')
                else:
                    messages.error(request, "Contraseña incorrecta.")
            else:
                messages.error(request, "El correo electrónico no está registrado.")
    else:
        form = LoginForm()
    return render(request, 'vinoteca_app/auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


class ListaVinosExternosAPIView(APIView):
    def get(self, request):
        url_externa = "https://api.sampleapis.com/wines/reds"
        try:
            respuesta = requests.get(url_externa, timeout=5)
            if respuesta.status_code == 200:
                datos_raw = respuesta.json()[:3]

                serializer = VinoExternoSerializer(data=datos_raw, many=True)
                if serializer.is_valid():
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "No se pudo conectar a la API externa"}, status=respuesta.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def productos(request):
    api_url = "http://127.0.0.1:8000/api/vinos-externos/"
    vinos_api = []

    try:
        res = requests.get(api_url, timeout=3)
        if res.status_code == 200:
            vinos_api = res.json()
    except:
        pass

    return render(request, 'vinoteca_app/productos.html', {'vinos_api': vinos_api})