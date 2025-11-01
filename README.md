# EMT Palma - Consulta de Tiempos de Llegada

Una aplicación de escritorio desarrollada en Python con PyQt6 que permite consultar los tiempos de llegada de los autobuses en las paradas de EMT Palma (Empresa Municipal de Transportes de Palma de Mallorca).

## 📋 Descripción

Esta aplicación conecta con la API pública de EMT Palma para mostrar información en tiempo real sobre las próximas llegadas de autobuses a cualquier parada del servicio. La interfaz es intuitiva y permite consultar rápidamente los tiempos de espera.

## 🏗️ Arquitectura

El proyecto sigue el patrón **Modelo-Vista-Controlador (MVC)**:

### 📁 Estructura del Proyecto

```
EMT/
├── main.py                    # Punto de entrada de la aplicación
├── model/
│   └── model_window.py        # Modelo: EMTApi (comunicación con la API)
├── view/
│   └── main_window.py         # Vista: Ui_MainWindow (interfaz de usuario)
├── controller/
│   └── controller_window.py   # Controlador: BusController (lógica de negocio)
└── uiEMT.ui                   # Archivo de diseño de Qt Designer
```

### Componentes

- **Model (`model_window.py`)**: Clase `EMTApi` que gestiona las peticiones HTTP a la API de EMT Palma. Se encarga de:
  - Obtener los tiempos de llegada de autobuses
  - Cargar los colores asociados a cada línea de autobús
  - Manejar errores de conexión y respuestas del servidor

- **View (`main_window.py`)**: Clase `Ui_MainWindow` que define la estructura visual de la aplicación:
  - Panel izquierdo: Campo de entrada para el número de parada, botón de consulta e historial de paradas recientes
  - Panel derecho: Área de desplazamiento que muestra las llegadas de autobuses

- **Controller (`controller_window.py`)**: Clase `BusController` que conecta la vista con el modelo:
  - Gestiona los eventos de la interfaz
  - Procesa las consultas de paradas
  - Mantiene un historial de las últimas 6 paradas consultadas
  - Formatea y muestra los resultados en la vista

## ✨ Características

- 🚌 **Consulta de paradas**: Introduce el número de parada para ver los próximos autobuses
- 🎨 **Líneas con colores**: Cada línea de autobús se muestra con su color oficial
- 📋 **Historial de paradas**: Guarda las últimas 6 paradas consultadas para acceso rápido
- ⏱️ **Tiempos en tiempo real**: Muestra los minutos hasta la llegada del autobús (o "YA" si está llegando)
- 🔄 **Manejo de errores**: Gestiona problemas de conexión, paradas inválidas y tokens caducados
- 🕐 **Última actualización**: Muestra cuándo se realizó la última consulta exitosa

## 📦 Requisitos

- Python 3.7 o superior
- PyQt6
- requests

## 🚀 Instalación

1. Clona o descarga este repositorio

2. Instala las dependencias necesarias:

```bash
pip install PyQt6 requests
```

## 💻 Uso

1. Ejecuta la aplicación:

```bash
python main.py
```

2. En la interfaz:
   - Introduce el número de parada en el campo de texto
   - Haz clic en "Consultar parada" o presiona Enter
   - Los resultados se mostrarán en el panel derecho con:
     - Número de línea (con su color oficial)
     - Destino del autobús
     - Tiempo de llegada en minutos

3. **Historial**: Las paradas consultadas aparecerán como botones en el panel izquierdo. Haz clic en cualquiera para consultarla de nuevo rápidamente.

## ⚙️ Configuración

### Token de Autenticación

La aplicación utiliza un token Bearer para autenticarse con la API de EMT Palma. Este token está definido en `model/model_window.py`:

```python
TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzM4NCJ9..."
```

**⚠️ Nota**: Si el token caduca (código 401), necesitarás obtener uno nuevo actualizando el valor de `TOKEN` en la clase `EMTApi`.

## 🔧 Funcionamiento Técnico

### Flujo de la Aplicación

1. El usuario introduce un número de parada
2. El controlador valida que sea un número válido
3. El controlador solicita al modelo que obtenga las llegadas
4. El modelo realiza una petición GET a la API de EMT Palma
5. Los datos se procesan y formatean
6. El controlador actualiza la vista con los resultados
7. Se guarda la parada en el historial reciente

### API Endpoints Utilizados

- **Colores de líneas**: `https://www.emtpalma.cat/maas/api/v1/agency/stops/`
- **Tiempos de llegada**: `https://www.emtpalma.cat/maas/api/v1/agency/stops/{stop_id}/timestr`

### Manejo de Errores

La aplicación maneja varios escenarios de error:
- `no_internet`: Problemas de conexión o servidor no disponible
- `invalid_stop`: La parada no existe o no tiene autobuses programados
- `token_expired`: El token de autenticación ha caducado

## 📝 Licencia

Este proyecto es de uso educativo y está destinado a fines académicos.

## 👨‍💻 Autor

Proyecto desarrollado para el módulo de **Interfaces** del ciclo formativo **DAM (Desarrollo de Aplicaciones Multiplataforma)** - CIFP Inca.

---

**Nota**: Esta aplicación utiliza la API pública de EMT Palma. Asegúrate de cumplir con sus términos de uso y políticas de acceso.

