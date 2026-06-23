from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactoForm
from .models import Contacto

def home(request):
    return render(request, 'vinoteca_app/index.html')

def nosotros(request):
    return render(request, 'vinoteca_app/nosotros.html')

def productos(request):
    return render(request, 'vinoteca_app/productos.html')

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

