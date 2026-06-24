# Vinoteca

## Gestión de Solicitudes y Panel Interno (REQ 6)
Para validar el panel de administración y comprobar la persistencia de los datos en PostgreSQL, se puede acceder de dos maneras:

1. **Desde la interfaz del sitio**: Utilizando el acceso directo visible ubicado en el pie de página (`footer.html`) rotulado como **🔒**.
2. **De forma directa**: Navegando a la URL correspondiente `/admin/`.

### Credenciales de Acceso de Superusuario (Entorno Local):

* **Usuario:** `admin`
* **Contraseña:** `admin`

### Credenciales de Acceso de Superusuario (Entorno de Producción - Render):
Para el acceso al panel administrativo una vez publicado el proyecto en la web a través de Render, se deben utilizar las siguientes credenciales de producción:
* **Usuario:** `postgres`
* **Contraseña:** `Django`

## Guía de Reproducción del Entorno Administrativo
En caso de que la base de datos se despliegue limpia o se requiera inicializar el sistema de autenticación de Django desde cero en un nuevo entorno, se debe ejecutar el siguiente comando interactivo en la terminal del proyecto:

```bash
python manage.py createsuperuser
```

### Instrucciones de Configuración en la Terminal:
1. Al ejecutar el comando, el sistema solicitará un **Username** (ej: `admin`).
2. Luego requerirá una dirección de **Email** (puede dejarse en blanco presionando `Enter`).
3. Finalmente, solicitará la **Password**. Coloque la contraseña (ej: `admin`) y presione `Enter` para confirmar.

Una vez que la terminal devuelva el mensaje **Superuser created successfully**, el panel `/admin/` estará completamente operativo con el nuevo usuario.