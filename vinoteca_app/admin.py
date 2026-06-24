from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from .models import Contacto
from .models import UsuarioPermitido, PerfilUsuario

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asunto', 'fecha_envio')
    list_filter = ('asunto', 'fecha_envio')
    search_fields = ('nombre', 'email', 'mensaje')
    ordering = ('-fecha_envio',)
    readonly_fields = ('mensaje', 'fecha_envio')

    def changelist_view(self, request, extra_context=None):
        queryset = self.get_queryset(request)

        ctx_estadisticas = {
            'total': queryset.count(),
            'comercial': queryset.filter(categoria="Consulta Comercial").count(),
            'tecnica': queryset.filter(categoria="Consulta Técnica").count(),
            'rrhh': queryset.filter(categoria="Consulta de RRHH").count(),
            'general': queryset.filter(categoria="Consulta General").count(),
        }

        html_renderizado = render_to_string(
            'vinoteca_app/admin/resumen_estadisticas.html',
            {'estadisticas': ctx_estadisticas}
        )

        extra_context = extra_context or {}
        extra_context['resumen_estadisticas'] = mark_safe(html_renderizado)

        return super().changelist_view(request, extra_context=extra_context)

@admin.register(UsuarioPermitido)
class UsuarioPermitidoAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre', 'codigo_validation')
    search_fields = ('email', 'nombre')

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'cuenta_validada')
    list_filter = ('cuenta_validada',)