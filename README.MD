Módulo de Gestión de Biblioteca (Odoo 16)
Este módulo personalizado para Odoo 16 permite la gestión integral de una biblioteca, permitiendo administrar libros, autores, géneros y el ciclo de vida de los préstamos a socios.

🛡️ Seguridad y Roles de UsuarioEste módulo implementa un control de acceso basado en grupos (RBAC). Los permisos están divididos en dos niveles de acceso dentro de la categoría Biblioteca.

👥 Grupos Disponibles:
Usuario Biblioteca - Create, Read, Update
Administrador Biblioteca - Create, Read, Update, Delete

⚙️ Cómo asignar permisos a un usuario.

Para asignar estos roles a un usuario en Odoo, sigue estos pasos:

1.- Activar el Modo Desarrollador: Ve a Ajustes y haz clic en "Activar modo desarrollador".
2.- Acceder a Usuarios: Dirígete a Ajustes > Usuarios y compañías > Usuarios.
3.- Seleccionar Usuario: Abre la ficha del usuario al que deseas dar acceso.
4.- Localizar Sección Biblioteca: En la pestaña Permisos, busca el apartado titulado Biblioteca.
5.- Seleccionar Nivel: Elige entre Usuario Biblioteca o Administrador Biblioteca en el menú desplegable.
6.- Guardar: Haz clic en el botón de guardar. El usuario deberá refrescar el navegador para ver los nuevos menús.

📄 Resumen Técnico de Accesos (ir.model.access)Los permisos definidos en el archivo ir.model.access.csv aseguran la integridad de los datos impidiendo el borrado accidental por parte de los usuarios:Modelos afectados: Autor, Libro, Género y Préstamo.Restricción Crítica: El permiso de Unlink (perm_unlink) está configurado en 0 para el grupo group_biblioteca_user en todos los modelos, garantizando que solo los administradores puedan eliminar registros del sistema.

🚀 Características Principales
Gestión de Catálogo: Control detallado de libros (ISBN, editorial, año de publicación) con estados dinámicos (Disponible, Prestado, Reparación, Perdido).

Relación Avanzada Autor-Libro: Soporte para múltiples autores por libro con designación de Autor Principal y orden de aparición.

Sistema de Préstamos: Registro de préstamos vinculado a los contactos de Odoo (res.partner), con cálculo automático de fechas de devolución y control de estados.

Clasificación por Géneros: Categorización mediante etiquetas de colores y normalización automática de nombres (conversión a mayúsculas).

Integración con Contactos: Extensión del modelo nativo de Odoo para identificar y gestionar socios de la biblioteca.

🛠️ Estructura de Datos:

<details>
  <summary><b>📂 Ver estructura del proyecto (clic para desplegar)</b></summary>

```text
biblioteca/
├── .gitignore
├── __init__.py
├── __manifest__.py
├── README.MD
├── controllers/
│   ├── __init__.py
│   └── controllers.py
├── data/
│   └── cron.xml
├── documentacion/
│   ├── Diag-ENT-REL.html
│   └── Diag-ENT-REL.pdf
├── models/
│   ├── __init__.py
│   ├── autor.py
│   ├── autor_libro.py
│   ├── genero.py
│   ├── libro.py
│   ├── prestamo.py
│   └── res_partner.py
├── views/
│   ├── autor.xml
│   ├── autor_libro.xml
│   ├── genero.xml
│   ├── libro.xml
│   ├── prestamo.xml
│   ├── res_partner.xml
│   └── secuencia_data.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
└── static/
    └── description/
        └── icon.png
```

</details>

El módulo se basa en los siguientes modelos técnicos:

📚 Libros y Autores
biblioteca.libro: Almacena la información técnica y física de los ejemplares.

biblioteca.autor: Directorio de autores con biografía y fotografía.

biblioteca.autor_libro: Modelo intermedio para gestionar la relación compleja entre autores y libros, permitiendo definir quién es el autor principal.

🏷️ Categorización y Préstamos
biblioteca.genero: Taxonomía de libros con validaciones de unicidad y formato.

biblioteca.prestamo: Registro de movimientos de salida y entrada de libros.

res.partner (Extensión): Se añade el campo es_socio_biblioteca para habilitar a los contactos como usuarios de la biblioteca.

⚙️ Validaciones y Lógica de Negocio
El módulo incluye lógica automatizada para garantizar la integridad de los datos:

Validación de Fechas: No se permite que el año de publicación o la fecha de adquisición sean posteriores a la fecha actual.

Normalización de Géneros: Los nombres de los géneros se convierten automáticamente a MAYÚSCULAS mediante api.onchange y overrides en los métodos create y write.

Reglas de Unicidad (SQL Constraints):

ISBN único por libro.

Nombre de género único.

Evita la duplicidad de un mismo autor en un mismo libro.

Cálculo de Fechas: El sistema sugiere automáticamente una fecha de devolución prevista (15 días por defecto).

📋 Requisitos e Instalación
Dependencias
Este módulo es independiente, aunque extiende el modelo base:

base (Odoo Standard)

Instalación
Copia la carpeta del módulo en tu directorio de custom-addons.

Actualiza la lista de aplicaciones en el modo desarrollador de Odoo.

Busca "Biblioteca" e instálalo.

📝 Notas de Desarrollo
Versión de Odoo: 16.0


Seguridad: Se han implementado dominios en los campos de búsqueda (ej. solo libros "disponibles" pueden ser seleccionados en nuevos préstamos).

🖥️ Interfaz de Usuario y Experiencia (UX)
El módulo explota las capacidades visuales de Odoo 16 para ofrecer una gestión intuitiva y moderna:

🎴 Vista Kanban (Libros)
Se ha implementado una vista Kanban rica visualmente para el catálogo de libros que incluye:

Tarjetas dinámicas: Muestran la portada del libro, editorial e ISBN.

Badges de Estado: Etiquetas de colores (Bootstrap) que cambian según el estado del libro (Verde para disponible, Azul para prestado, Naranja para reparación y Rojo para perdido).

Optimización Mobile: Diseño adaptativo para dispositivos móviles mediante la clase o_kanban_mobile.

📄 Vistas de Formulario Avanzadas
Los formularios utilizan elementos de organización complejos para mejorar la carga de datos:

Uso de Avatares: Tanto en Libros como en Autores, se utiliza el widget image con la clase oe_avatar para una gestión visual de portadas y fotografías.

Organización en Notebooks: La información se divide en pestañas (Información General, Autores, Histórico) para no saturar la vista principal.

Modelos Intermedios: En la pestaña de autores, se permite gestionar el orden de los autores mediante un widget de arrastre (handle) y marcar la autoría principal directamente desde la ficha del libro.

📊 Componentes y Widgets Técnicos
Widget Badge: En las vistas de lista (Tree), el estado del libro utiliza widget="badge" con decoraciones condicionales (decoration-success, decoration-danger, etc.).

Color Picker: El modelo de Géneros integra un selector de colores (widget="color_picker") para categorizar visualmente las etiquetas.

Many2Many Tags: Los géneros se visualizan en el libro como etiquetas compactas para ahorrar espacio.

🔍 Potencia de Búsqueda
La vista de búsqueda (search) permite una segmentación profunda:

Filtros por Estado: Acceso con un solo clic a libros disponibles, prestados, en reparación o perdidos.

Agrupación Dinámica: Capacidad de reorganizar la lista completa de libros por su Estado de forma automática.

🔄 Gestión de Préstamos (Flujo de Trabajo)
La vista de Préstamos es el centro operativo del módulo y destaca por:

Barra de Ciclo de Vida (statusbar): Implementación de una barra de estados interactiva (Activo, Retrasado, Devuelto) que permite visualizar y cambiar el progreso del préstamo.

Botones de Acción Inteligentes:

Devolución Libro: Botón destacado (btn-success) para finalizar el préstamo.

Renovación Dinámica: Botón para extender la fecha de entrega 15 días automáticamente.

Control de Visibilidad (attrs): Los botones aparecen o desaparecen dinámicamente según el estado (ej. el botón de devolución se oculta si el libro ya ha sido devuelto).

Cabecera Informativa: Uso de contenedores Flexbox para mostrar de forma clara la Referencia, Fecha de Entrega y número de Renovaciones en la parte superior del formulario.

👥 Integración y Herencia (Socios)
El módulo no crea un modelo de contactos desde cero, sino que extiende el ecosistema nativo de Odoo:

Herencia de Vistas (res.partner): Se inyectan campos personalizados en las vistas estándar de Odoo mediante xpath.

Widget boolean_toggle: Implementación de interruptores modernos para marcar a un contacto como "Socio de Biblioteca" de forma rápida desde la vista de lista o formulario.

Histórico Integrado: Se ha añadido una pestaña (Page) adicional en la ficha del contacto que muestra todos sus préstamos pasados y presentes, centralizando la información del socio.

🔍 Vistas de Búsqueda Avanzada
Filtros de Préstamos: Segmentación por préstamos con retraso o devueltos.

Agrupación por Socio: Permite a los bibliotecarios ver rápidamente cuántos libros tiene cada socio bajo su responsabilidad.

Contextos Predeterminados: La acción de "Socios" está configurada para mostrar por defecto solo a los contactos que tienen activado el check de biblioteca (search_default_es_socio_biblioteca_filter).

🛠️ Aspectos Técnicos Destacados
Herencia de Modelos y Vistas: Uso de _inherit para ampliar res.partner sin romper la compatibilidad con otros módulos de Odoo (Ventas, Facturación, etc.).

Vistas Dinámicas: Uso extensivo de atributos readonly y invisible basados en estados para evitar errores de usuario.

Normalización de Datos: Los nombres de los géneros se limpian y pasan a mayúsculas automáticamente antes de guardarse.

🔐 Integridad de Estados
El sistema incluye controles de flujo de estados para evitar inconsistencias físicas:

Restricción de Libros en Uso: Un libro con estado Prestado tiene bloqueada la transición a Reparación o Perdido. Esta validación garantiza que no se pierda la trazabilidad de un préstamo activo, obligando a procesar la devolución antes de cambiar la ubicación física o estado del ejemplar.

📝 GitHub de la aplicación: 
https://github.com/rafaelgor-1978/biblioteca-odoo16


