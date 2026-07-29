from .forms import ContactoForm, RegistroForm, ValidacionCodigoForm, LoginForm, CMSNosotrosForm
from .models import Contacto, UsuarioPermitido, PerfilUsuario, ContenidoNosotros
from .serializers import VinoExternoSerializer
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
from django.views import View
from django.urls import reverse
from .forms import ContactoEdicionForm
from django.db import IntegrityError, connection
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import os

def home(request):
    return render(request, 'vinoteca_app/index.html')

def nosotros(request):
    contenido, _ = ContenidoNosotros.objects.get_or_create(id=1)
    return render(request, 'vinoteca_app/nosotros.html', {'contenido': contenido})

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
            except IntegrityError:
                # Si PostgreSQL se desincronizó por borrados previos,
                # corrijo la secuencia automáticamente desde el código
                with connection.cursor() as cursor:
                    cursor.execute("SELECT setval(pg_get_serial_sequence('vinoteca_app_contacto', 'id'), coalesce(max(id), 1)) FROM vinoteca_app_contacto;")
                
                # Volvemos a intentar el guardado de forma segura
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
                if request.user.is_authenticated and request.user.email:
                    destinatario_final = request.user.email
                    nombre_destinatario = request.user.first_name or request.user.username
                else:
                    destinatario_final = 'skalapuj@gmail.com'
                    nombre_destinatario = "Profesora Analía"

                asunto_legible = dict(form.fields['asunto'].choices).get(datos_limpios['asunto'], 'Consulta General')

                asunto_mail = f"Nueva Consulta Recibida - Categoría: {nueva_consulta.categoria}"

                cuerpo_mensaje = render_to_string('emails/email_contacto.html', {
                    'nombre_destinatario': nombre_destinatario,
                    'datos': datos_limpios,
                    'asunto_legible': asunto_legible,
                    'nueva_consulta': nueva_consulta
                });

                if settings.DEBUG:
                    # Si NO estoy en Render (o sea, estamos en localhost), mando el mail
                    texto_plano = strip_tags(cuerpo_mensaje)
                    email = EmailMultiAlternatives(
                        subject=asunto_mail,
                        body=texto_plano,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[destinatario_final],
                    )
                    email.attach_alternative(cuerpo_mensaje, "text/html")
                    email.send(fail_silently=False)

                print(f"Correo automático de categoría [{nueva_consulta.categoria}] enviado con éxito a: {destinatario_final}")

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
                        try:
                            request.session['email_a_validar'] = email_ingresado
                            asunto_reenvio = "Reenvío de Código de Validación - Panel de Administración Vinoteca Reserva"
                            cuerpo_html_reenvio = render_to_string('emails/email_reenvio_codigo.html', {
                                'permitido': permitido
                            })

                            if settings.DEBUG:
                                # Si NO estoy en Render (o sea, estamos en localhost), mando el mail
                                texto_plano = strip_tags(cuerpo_html_reenvio)
                                email = EmailMultiAlternatives(
                                    subject=asunto_reenvio,
                                    body=texto_plano,
                                    from_email=settings.DEFAULT_FROM_EMAIL,
                                    to=[email_ingresado],
                                )
                                email.attach_alternative(cuerpo_html_reenvio, "text/html")
                                email.send(fail_silently=False)

                            return JsonResponse({
                                'status': 'success',
                                'message': 'La cuenta ya existe pero falta validar. Le reenviamos el correo.'
                            })
                        except Exception as e:
                            return JsonResponse({
                                'status': 'error',
                                'errors': [f"Error crítico al enviar el email: {str(e)}"]
                            }, status=500)

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

                    cuerpo_auth = render_to_string('emails/email_validacion.html', {
                        'permitido': permitido
                    })

                    if settings.DEBUG:
                        # Si NO estoy en Render (o sea, estamos en localhost), mando el mail
                        texto_plano = strip_tags(cuerpo_auth)
                        email = EmailMultiAlternatives(
                            subject=asunto_auth,
                            body=texto_plano,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[email_ingresado],
                        )
                        email.attach_alternative(cuerpo_auth, "text/html")
                        email.send(fail_silently=False)

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
                    return redirect('panel_consultas')
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
    api_url = request.build_absolute_uri(reverse('api_vinos_externos'))
    vinos_api = []

    try:
        api_view = ListaVinosExternosAPIView.as_view()
        response = api_view(request)
        if response.status_code == 200:
            vinos_api = response.data
    except Exception as e:
        print(f"Error interno al invocar la APIView de DRF: {e}")

    return render(request, 'vinoteca_app/productos.html', {'vinos_api': vinos_api})

@staff_member_required(login_url='login')
def cms_editor_view(request):
    contenido, _ = ContenidoNosotros.objects.get_or_create(id=1)

    if request.method == 'POST':
        form = CMSNosotrosForm(request.POST, instance=contenido)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Contenido de la página 'Nosotros' actualizado con éxito!")
            return redirect('cms_editor')
        else:
            messages.error(request, "Ocurrió un error al intentar guardar los cambios.")
    else:
        form = CMSNosotrosForm(instance=contenido)

    return render(request, 'vinoteca_app/admin/cms_editor.html', {
        'form': form,
        'contenido': contenido
    })

@staff_member_required(login_url='login')
def panel_consultas(request):
    consultas = Contacto.objects.all().order_by('-fecha_envio')
    
    ctx_estadisticas = {
        'total': consultas.count(),
        'comercial': consultas.filter(categoria="Consulta Comercial").count(),
        'tecnica': consultas.filter(categoria="Consulta Técnica").count(),
        'rrhh': consultas.filter(categoria="Consulta de RRHH").count(),
        'general': consultas.filter(categoria="Consulta General").count(),
    }
    
    return render(request, 'vinoteca_app/admin/panel_consultas.html', {
        'consultas': consultas,
        'estadisticas': ctx_estadisticas
    })

@staff_member_required(login_url='login')
def editar_consulta(request, pk):
    consulta = get_object_or_404(Contacto, pk=pk)
    
    if request.method == 'POST':
        form = ContactoEdicionForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, 'La consulta fue actualizada con éxito.')
            return redirect('panel_consultas')
    else:
        form = ContactoEdicionForm(instance=consulta)
        
    return render(request, 'vinoteca_app/admin/editar_consulta.html', {
        'form': form,
        'consulta': consulta
    })

@staff_member_required(login_url='login')
def eliminar_consulta(request, pk):
    consulta = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        consulta.delete()
        messages.success(request, 'La consulta ha sido eliminada correctamente.')
        return redirect('panel_consultas')
        
    return render(request, 'vinoteca_app/admin/eliminar_consulta.html', {'consulta': consulta})

def olvide_password_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()

            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                cuerpo_html = render_to_string('emails/email_restablecer_password.html', {
                    'user': user,
                    'domain': request.get_host(),
                    'protocol': 'https' if request.is_secure() else 'http',
                    'uid': uid,
                    'token': token,
                })
                texto_plano = strip_tags(cuerpo_html)

                try:
                    email_msg = EmailMultiAlternatives(
                        subject="Restablecimiento de Contraseña - Vinoteca Reserva",
                        body=texto_plano,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[email],
                    )
                    email_msg.attach_alternative(cuerpo_html, "text/html")
                    email_msg.send(fail_silently=False)

                    messages.success(request, f"Te hemos enviado un correo a {email} con las instrucciones para restablecer tu contraseña.")
                    return redirect('login')
                except Exception as e:
                    messages.error(request, f"Error al enviar el correo: {str(e)}")
            else:
                messages.error(request, "El correo electrónico ingresado no se encuentra registrado.")
    else:
        form = PasswordResetForm()
    return render(request, 'vinoteca_app/auth/olvide_password.html', {'form': form})

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'vinoteca_app/auth/reset_confirm.html'
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "¡Tu contraseña se ha restablecido con éxito! Ya puedes iniciar sesión.")
        return redirect('login')