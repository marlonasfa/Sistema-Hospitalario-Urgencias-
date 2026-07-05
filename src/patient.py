"""
Definición de la clase Patient para la simulación hospitalaria.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Patient:
    """Representa un paciente en el sistema de emergencias."""
    
    id: int
    priority_type: str  # 'EMERGENCY', 'URGENCY', 'CONSULTATION'
    arrival_time: float  # Tiempo de llegada en minutos
    priority_level: int  # Nivel de prioridad numérico
    service_time: float  # Tiempo de servicio requerido en minutos
    
    # Timestamps para seguimiento
    start_wait_time: Optional[float] = None
    start_service_time: Optional[float] = None
    end_service_time: Optional[float] = None
    
    # Estados
    abandoned: bool = False
    abandon_time: Optional[float] = None
    served: bool = False
    
    # Estadísticas
    waiting_time: float = field(default=0.0)
    total_time_in_system: float = field(default=0.0)
    
    def __lt__(self, other):
        """Comparación para prioridad en la cola."""
        if self.priority_level != other.priority_level:
            return self.priority_level < other.priority_level
        return self.arrival_time < other.arrival_time
    
    def get_priority_name(self) -> str:
        """Retorna el nombre legible de la prioridad."""
        priority_map = {
            'EMERGENCY': 'EMERGENCIA',
            'URGENCY': 'URGENCIA',
            'CONSULTATION': 'CONSULTA'
        }
        return priority_map.get(self.priority_type, 'DESCONOCIDA')
    
    def __str__(self) -> str:
        """Representación en string del paciente."""
        return (f"Paciente #{self.id:04d} | Prioridad: {self.get_priority_name()} | "
                f"Llegada: {self.arrival_time:.2f} min")
