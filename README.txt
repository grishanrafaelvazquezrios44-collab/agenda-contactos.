AGENDA CONTACTLY - Flask + SQLite

FUNCIONES
- Agregar, consultar, editar y eliminar contactos.
- Buscar por nombre, teléfono o correo.
- Filtrar por categoría y ver favoritos.
- Marcar y quitar favoritos.
- Guardar cumpleaños y notas.
- Acceso rápido para llamar desde el celular.
- Exportar contactos a CSV.
- Panel con estadísticas.
- Diseño adaptable a celular y computadora.

EJECUTAR EN PYDROID 3
1. Instala Flask y Gunicorn desde Pip (Gunicorn solo se necesita para Render).
2. Abre app.py y ejecútalo.
3. En Chrome abre http://127.0.0.1:5000

IMPORTANTE SOBRE LOS CONTACTOS ANTERIORES
La base de datos contactos.db se crea automáticamente. Si quieres conservar los contactos
de tu versión anterior, copia tu archivo contactos.db anterior dentro de esta carpeta antes
de ejecutar app.py. La aplicación agrega las columnas nuevas sin borrar los datos anteriores.

PUBLICAR EN RENDER
Sube todos los archivos a un repositorio de GitHub y crea un Web Service en Render.
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app

NOTA: SQLite guarda los datos en un archivo local. En Render, para conservar datos entre
reinicios y despliegues, configura un Persistent Disk y guarda la base de datos en ese disco.
