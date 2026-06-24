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

## API Propia
El proyecto cuenta con una API interna desarrollada con **Django REST Framework (DRF)** que expone las solicitudes recibidas a través del formulario del sitio web en formato JSON.

- **Ruta Base de la API:** `http://127.0.0.1:8000/api/`
- **Punto de End-point Solicitado:** `/api/consultas/`
- **URL Completa de Acceso:** [http://127.0.0.1:8000/api/consultas/](http://127.0.0.1:8000/api/consultas/)

### Métodos HTTP 
- `GET /api/consultas/`: Retorna el listado completo de todas las consultas almacenadas en la base de datos en formato JSON.

### Formato de Respuesta (JSON Ejemplo)
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "asunto": "Consulta sobre Vinos Reservados",
    "mensaje": "Me gustaría recibir más información sobre el catálogo de tintos.",
    "fecha_envio": "2026-06-24T12:00:00Z"
  }
]
```
## 🌐 Consumo de API Externa con Django REST Framework (DRF)
- **URL de la API:** https://api.sampleapis.com/wines/reds
- **Descripción:** Provee un listado en formato JSON de vinos tintos del mundo, incluyendo bodega, nombre del vino, calificaciones y locación.
- **Implementación:** Consumida desde el backend mediante la librería `requests` de Python e integrada en el sistema de templates de Django.

### ⚙️ Arquitectura y Flujo de Datos
El circuito de información se diseñó bajo una arquitectura limpia de backend distribuyendo las responsabilidades en las siguientes capas:
```
[API Externa: SampleAPIs]
│
▼ ( requests.get )
[Backend: ListaVinosExternosAPIView (DRF)] ──► [VinoExternoSerializer (Validación)]
│
▼ ( Petición Interna )
[Django View: productos_view] ──► Inyección en Contexto ──► [Template: productos.html]
│
▼
[Navegador del Cliente]
```
1. **Capa de Consumo (Python Requests):** Al procesar la vista, el servidor de Django realiza una petición HTTP asíncrona hacia la API externa mediante la librería `requests`, abstrayendo las credenciales y el consumo del cliente.
2. **Capa de Serialización (DRF Serializers):** Los datos *raw* obtenidos (JSON) ingresan a la clase `VinoExternoSerializer`. DRF se encarga de validar la estructura del formato, tipar los datos y realizar un *slice* quirúrgico para procesar únicamente los primeros 6 registros de guarda, optimizando la transferencia.
3. **Capa de Exposición (DRF APIView):** Se generó un endpoint interno propio (`/api/vinos-externos/`) mediante una `APIView` de REST Framework, aislando el comportamiento de la API del resto de la aplicación.
4. **Capa de Renderizado (Django Templates):** La vista tradicional `productos_view` toma los datos limpios provistos por el endpoint de DRF y los inyecta de forma nativa en el servidor usando las directivas del motor de plantillas (`{% for vino in vinos_api %}`).
5. **Capa de Interacción Visual (JavaScript Local):** El navegador recibe el HTML ya estructurado y pintado con los datos. JavaScript se limita única y exclusivamente a manejar el comportamiento estético de la interfaz (abrir y cerrar el componente modal `wine-modal` al disparar el evento `click` en los botones de detalles), delegando el 100% de la lógica de datos al backend.