# Copa Renault App

Aplicación web para la gestión de la Copa Renault, desarrollada con Flask y Bootstrap. Permite la administración de usuarios, equipos, fixtures, reservas de cantina y sponsors, con una interfaz moderna, responsiva y segura.

## Características principales

- Registro e inicio de sesión seguro con roles diferenciados (administrador, entrenador, jugador).
- Gestión de equipos: alta, modificación y baja.
- Generación y visualización de fixtures por deporte y categoría.
- Reservas de servicios de cantina con gestión de restricciones dietarias.
- Página de sponsors con enlaces y logos.
- Panel de administración para la gestión de datos.
- Interfaz intuitiva, adaptativa y visualmente atractiva.
- Seguridad: encriptación de contraseñas y preparado para HTTPS.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/mateo-ulla/App-Copa-Renault
   cd CopaRenaultApp
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   python app.py
   ```
4. Accede desde tu navegador a [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Estructura del proyecto

- `app.py`: Archivo principal de la aplicación Flask.
- `models.py`: Definición de modelos y base de datos.
- `routes.py`: Rutas y lógica de negocio.
- `config.py`: Configuración de la app.
- `templates/`: Archivos HTML (Jinja2).
- `static/`: Archivos estáticos (CSS, JS, imágenes).
- `requirements.txt`: Dependencias del proyecto.
