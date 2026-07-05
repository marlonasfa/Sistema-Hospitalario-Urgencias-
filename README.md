# Simulación del Sistema Hospitalario de Urgencias

**Proyecto de Optimización y Simulación de Sistemas**  
Universidad Privada San Juan Bautista - Ingeniería de Sistemas  
Semestre 2026-I

## 📋 Descripción

Este proyecto implementa una simulación del área de emergencias de un hospital utilizando **SimPy** (Python Simulation Library). La simulación modela el funcionamiento real del sistema con llegadas aleatorias de pacientes, tres niveles de prioridad y recursos limitados (médicos, enfermeras y camas).

Incluye una **interfaz web profesional** con dashboard interactivo para visualizar resultados en tiempo real.

## 🎯 Objetivos

- Simular el funcionamiento del área de emergencias de un hospital
- Calcular métricas de rendimiento del sistema
- Analizar la utilización de recursos
- Determinar patrones de espera y abandono de pacientes
- Proporcionar una interfaz amigable para visualización de resultados

## 🏥 Características del Sistema

### Llegadas de Pacientes
- **Aleatorias**: Distribuidas exponencialmente
- **Tres niveles de prioridad**:
  - 🔴 **Emergencia**: Prioridad máxima (tiempo máximo espera: 60 min)
  - 🟠 **Urgencia**: Prioridad media (tiempo máximo espera: 45 min)
  - 🟡 **Consulta**: Prioridad baja (tiempo máximo espera: 30 min)

### Recursos Disponibles
- 👨‍⚕️ **3 Médicos** (PriorityResource)
- 👩‍⚕️ **5 Enfermeras** (PriorityResource)
- 🛏️ **8 Camas** (PriorityResource)

### Comportamientos del Sistema
- Si no hay camas disponibles, el paciente espera en la cola
- Si un paciente espera más del tiempo máximo permitido, abandona el sistema
- Los recursos se asignan según prioridad del paciente

## 📊 Métricas Calculadas

El sistema recopila y reporta:

1. **Tiempo promedio de espera por prioridad**
   - Emergencia
   - Urgencia
   - Consulta

2. **Utilización de recursos**
   - Utilización de médicos (%)
   - Utilización de enfermeras (%)
   - Utilización de camas (%)

3. **Estadísticas de pacientes**
   - Cantidad de pacientes atendidos
   - Cantidad de pacientes que abandonaron
   - Porcentaje de pacientes atendidos vs. abandonados

## 📁 Estructura del Proyecto

```
PC4_RIVERA_OP/
├── config/
│   └── settings.py                  # Parámetros de configuración
├── src/
│   ├── patient.py                   # Clase Patient
│   ├── statistics.py                # Recolector de estadísticas
│   └── hospital_simulation.py       # Simulador principal con SimPy
├── static/
│   ├── css/
│   │   └── style.css               # Estilos del dashboard
│   └── js/
│       └── app.js                  # Lógica del dashboard (JavaScript)
├── templates/
│   └── index.html                  # Interfaz web HTML
├── results/                         # Carpeta para resultados
├── main.py                          # Script de línea de comandos
├── app.py                           # Aplicación Flask
├── run_web.py                       # Script para ejecutar servidor web
├── requirements.txt                 # Dependencias
└── README.md                        # Este archivo
```

## 🚀 Instalación y Uso

### Requisitos Previos
- Python 3.8+
- pip (gestor de paquetes Python)

### Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd PC4_RIVERA_OP
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

### ✨ OPCIÓN 1: INTERFAZ WEB (Recomendada para el docente)

Ejecutar la aplicación web profesional:
```bash
python run_web.py
```

Luego acceder a: **http://localhost:5000**

El navegador se abrirá automáticamente. Puedes:
- ✅ Ejecutar simulaciones con un clic
- ✅ Ver resultados en tiempo real
- ✅ Visualizar gráficos interactivos
- ✅ Descargar resultados en JSON
- ✅ Imprimir reportes
- ✅ Ver estadísticas detalladas

### 📱 OPCIÓN 2: LÍNEA DE COMANDOS

Ejecutar la simulación desde terminal:
```bash
python main.py
```

O ejecutar directamente el simulador:
```bash
python -m src.hospital_simulation
```

## 📈 Resultados

### Desde la Interfaz Web
- Dashboard con 4 tarjetas de estadísticas principales
- Gráficos interactivos (pie chart y bar chart)
- Barras de progreso para utilización de recursos
- Botones para descargar JSON e imprimir reportes
- Información de tiempo de espera por prioridad

### Desde Línea de Comandos
Los resultados se guardan en la carpeta `results/`:

- **estadisticas_YYYYMMDD_HHMMSS.json**: Estadísticas en formato JSON
- **logs_YYYYMMDD_HHMMSS.txt**: Detalles de eventos de la simulación

## 🔧 Configuración

Para modificar los parámetros de la simulación, editar `config/settings.py`:

```python
SIMULATION_TIME = 480          # Duración en minutos
NUM_DOCTORS = 3                # Cantidad de médicos
NUM_NURSES = 5                 # Cantidad de enfermeras
NUM_BEDS = 8                   # Cantidad de camas
ARRIVAL_RATES = {...}          # Tasas de llegada por tipo
SERVICE_TIMES = {...}          # Tiempos de servicio
MAX_WAITING_TIME = {...}       # Tiempos máximos de espera
```

## 💡 Conceptos SimPy Utilizados

- **`PriorityResource`**: Para asignar médicos, enfermeras y camas con prioridad
- **`Resource`**: Alternativa para recursos sin prioridad
- **`Eventos`**: Manejo de procesos y sincronización
- **`Environment`**: Entorno de simulación principal
- **`Timeout`**: Para tiempos de espera máximos y servicios

## 🌐 Acceso Remoto (Para el docente en otra red)

Si deseas que el docente acceda desde otra computadora:

1. Ejecuta: `python run_web.py`
2. Obtén tu IP local:
   - **Windows**: Ejecuta `ipconfig` en terminal → busca "IPv4 Address"
   - **Linux/Mac**: Ejecuta `ifconfig` → busca "inet"
3. Comparte con el docente: **http://TU_IP:5000**
4. El docente accede desde su navegador usando esa dirección

## 📝 Ejemplo de Salida

```
================================================================================
SIMULACIÓN DEL SISTEMA HOSPITALARIO DE URGENCIAS
Universidad Privada San Juan Bautista - 2026-I
Asignatura: Optimización y Simulación de Sistemas
================================================================================

🏥 Iniciando simulación del Sistema Hospitalario de Urgencias...
   Duración: 480 minutos
   Recursos: 3 médicos, 5 enfermeras, 8 camas

✅ Simulación completada

================================================================================
REPORTE FINAL - SIMULACIÓN DEL SISTEMA HOSPITALARIO DE URGENCIAS
================================================================================

📊 ESTADÍSTICAS GENERALES:
  • Pacientes atendidos: 61
  • Pacientes que abandonaron: 0
  • Total de pacientes: 61
  • Porcentaje atendido: 100.00%
  • Porcentaje que abandonó: 0.00%

⏱️  TIEMPO PROMEDIO DE ESPERA POR PRIORIDAD:
  • Emergencia: 0.85 minutos
  • Urgencia: 7.08 minutos
  • Consulta: 0.19 minutos

👨‍⚕️  UTILIZACIÓN DE MÉDICOS: 90.82%

👩‍⚕️  UTILIZACIÓN DE ENFERMERAS: 54.49%

🛏️  UTILIZACIÓN DE CAMAS: 70.47%

================================================================================
```

## 👨‍💻 Autor

**Nombre del Estudiante**: [Completar con tu nombre]  
**Código de Estudiante**: [Completar con tu código]  
**Docente**: Mg. Huerta Rojas, Miguel Angel  
**Sede**: Chorrillos  
**Fecha**: 04/07/2026

## 📚 Referencias

- SimPy Documentation: https://simpy.readthedocs.io/
- Python Official Documentation: https://docs.python.org/3/
- Flask Documentation: https://flask.palletsprojects.com/

## ✨ Características Principales

### 🎨 Interfaz Web
- ✅ Diseño profesional y responsivo
- ✅ Colores modernos con gradientes
- ✅ Animaciones suaves
- ✅ Iconos Bootstrap
- ✅ Gráficos interactivos con Chart.js
- ✅ Notificaciones de estado en tiempo real

### 🔧 Funcionalidades
- ✅ Ejecución de simulaciones con un clic
- ✅ Visualización en tiempo real
- ✅ Descarga de resultados (JSON)
- ✅ Impresión de reportes
- ✅ Información de configuración del sistema
- ✅ Health check del servidor

### 🏥 Sistema Hospitalario
- ✅ Simulación realista de urgencias
- ✅ 3 niveles de prioridad
- ✅ Asignación inteligente de recursos
- ✅ Sistema de abandono de pacientes
- ✅ Estadísticas completas
- ✅ Logs detallados de eventos

---

**Estado**: ✅ Proyecto completo, profesional y funcional  
**Última actualización**: 04/07/2026  
**Versión**: 1.0
