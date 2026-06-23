from django.contrib import admin
from .models import Contacto

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asunto', 'fecha_envio')
    list_filter = ('asunto', 'fecha_envio')
    search_fields = ('nombre', 'email', 'mensaje')
    ordering = ('-fecha_envio',)
    readonly_fields = ('nombre', 'email', 'asunto', 'mensaje', 'fecha_envio')

    def has_delete_permission(self, request, obj=None):
      return False

    def has_add_permission(self, request):
      return False