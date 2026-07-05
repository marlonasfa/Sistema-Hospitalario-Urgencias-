"""
Configuración de parámetros para la simulación del hospital.
Universidad Privada San Juan Bautista - Ingeniería de Sistemas
Optimización y Simulación de Sistemas - 2026-I
"""

# Parámetros de la simulación
SIMULATION_TIME = 480  # Minutos (8 horas de operación)
RANDOM_SEED = 42  # Para reproducibilidad

# Recursos disponibles
NUM_DOCTORS = 3
NUM_NURSES = 5
NUM_BEDS = 8

# Distribuciones de llegada de pacientes (por minuto)
# Pacientes por minuto: emergencia, urgencia, consulta
ARRIVAL_RATES = {
    'EMERGENCY': 0.5,    # ~30 pacientes por hora
    'URGENCY': 0.8,      # ~48 pacientes por hora
    'CONSULTATION': 1.2  # ~72 pacientes por hora
}

# Tiempos de atención en minutos (media y desviación estándar)
SERVICE_TIMES = {
    'EMERGENCY': {'mean': 15, 'std': 3},      # Rango: 12-18 min
    'URGENCY': {'mean': 10, 'std': 2},        # Rango: 8-12 min
    'CONSULTATION': {'mean': 5, 'std': 1}     # Rango: 4-6 min
}

# Tiempo máximo que un paciente espera antes de abandonar (en minutos)
# Si el paciente espera más de esto, abandona
MAX_WAITING_TIME = {
    'EMERGENCY': 60,      # No abandona generalmente
    'URGENCY': 45,        # Puede abandonar
    'CONSULTATION': 30    # Probablemente abandona
}

# Prioridades para PriorityResource (menor número = mayor prioridad)
PRIORITY = {
    'EMERGENCY': 1,
    'URGENCY': 2,
    'CONSULTATION': 3
}

# Configuración de reportes
REPORT_INTERVAL = 60  # Reporte cada 60 minutos
OUTPUT_DIR = 'results/'
