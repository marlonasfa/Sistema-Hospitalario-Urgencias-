"""
Gestión de estadísticas para la simulación hospitalaria.
"""
from typing import Dict, List
from dataclasses import dataclass, field
import json
from datetime import datetime


@dataclass
class StatisticsCollector:
    """Recolecta y procesa estadísticas de la simulación."""
    
    patients_served: List = field(default_factory=list)
    patients_abandoned: List = field(default_factory=list)
    doctor_usage_log: List = field(default_factory=list)
    nurse_usage_log: List = field(default_factory=list)
    bed_usage_log: List = field(default_factory=list)
    
    def add_served_patient(self, patient):
        """Registra un paciente atendido."""
        self.patients_served.append(patient)
    
    def add_abandoned_patient(self, patient):
        """Registra un paciente que abandonó la cola."""
        self.patients_abandoned.append(patient)
    
    def record_doctor_usage(self, time: float, doctors_busy: int, total_doctors: int):
        """Registra el uso de médicos."""
        self.doctor_usage_log.append({
            'time': time,
            'busy': doctors_busy,
            'total': total_doctors,
            'utilization': doctors_busy / total_doctors
        })
    
    def record_nurse_usage(self, time: float, nurses_busy: int, total_nurses: int):
        """Registra el uso de enfermeras."""
        self.nurse_usage_log.append({
            'time': time,
            'busy': nurses_busy,
            'total': total_nurses,
            'utilization': nurses_busy / total_nurses
        })
    
    def record_bed_usage(self, time: float, beds_occupied: int, total_beds: int):
        """Registra el uso de camas."""
        self.bed_usage_log.append({
            'time': time,
            'occupied': beds_occupied,
            'total': total_beds,
            'utilization': beds_occupied / total_beds
        })
    
    def calculate_average_waiting_time_by_priority(self) -> Dict[str, float]:
        """Calcula tiempo promedio de espera por prioridad."""
        waiting_times = {
            'EMERGENCY': [],
            'URGENCY': [],
            'CONSULTATION': []
        }
        
        for patient in self.patients_served:
            waiting_times[patient.priority_type].append(patient.waiting_time)
        
        averages = {}
        for priority, times in waiting_times.items():
            if times:
                averages[priority] = sum(times) / len(times)
            else:
                averages[priority] = 0.0
        
        return averages
    
    def calculate_average_utilization(self, usage_log: List) -> float:
        """Calcula utilización promedio."""
        if not usage_log:
            return 0.0
        
        total_utilization = sum(log['utilization'] for log in usage_log)
        return total_utilization / len(usage_log)
    
    def get_summary(self) -> Dict:
        """Retorna un resumen completo de estadísticas."""
        total_patients = len(self.patients_served) + len(self.patients_abandoned)
        
        return {
            'patients_served': len(self.patients_served),
            'patients_abandoned': len(self.patients_abandoned),
            'total_patients': total_patients,
            'served_percentage': (len(self.patients_served) / total_patients * 100) if total_patients > 0 else 0,
            'abandoned_percentage': (len(self.patients_abandoned) / total_patients * 100) if total_patients > 0 else 0,
            'average_waiting_time_by_priority': self.calculate_average_waiting_time_by_priority(),
            'average_doctor_utilization': self.calculate_average_utilization(self.doctor_usage_log),
            'average_nurse_utilization': self.calculate_average_utilization(self.nurse_usage_log),
            'average_bed_utilization': self.calculate_average_utilization(self.bed_usage_log),
            'doctor_utilization_percent': self.calculate_average_utilization(self.doctor_usage_log) * 100,
            'nurse_utilization_percent': self.calculate_average_utilization(self.nurse_usage_log) * 100,
            'bed_utilization_percent': self.calculate_average_utilization(self.bed_usage_log) * 100,
        }
    
    def print_report(self):
        """Imprime un reporte detallado de las estadísticas."""
        summary = self.get_summary()
        
        print("\n" + "="*80)
        print("REPORTE FINAL - SIMULACIÓN DEL SISTEMA HOSPITALARIO DE URGENCIAS")
        print("="*80)
        
        print("\n📊 ESTADÍSTICAS GENERALES:")
        print(f"  • Pacientes atendidos: {summary['patients_served']}")
        print(f"  • Pacientes que abandonaron: {summary['patients_abandoned']}")
        print(f"  • Total de pacientes: {summary['total_patients']}")
        print(f"  • Porcentaje atendido: {summary['served_percentage']:.2f}%")
        print(f"  • Porcentaje que abandonó: {summary['abandoned_percentage']:.2f}%")
        
        print("\n⏱️  TIEMPO PROMEDIO DE ESPERA POR PRIORIDAD:")
        waiting_times = summary['average_waiting_time_by_priority']
        print(f"  • Emergencia: {waiting_times['EMERGENCY']:.2f} minutos")
        print(f"  • Urgencia: {waiting_times['URGENCY']:.2f} minutos")
        print(f"  • Consulta: {waiting_times['CONSULTATION']:.2f} minutos")
        
        print("\n👨‍⚕️  UTILIZACIÓN DE MÉDICOS: {:.2f}%".format(summary['doctor_utilization_percent']))
        print("\n👩‍⚕️  UTILIZACIÓN DE ENFERMERAS: {:.2f}%".format(summary['nurse_utilization_percent']))
        print("\n🛏️  UTILIZACIÓN DE CAMAS: {:.2f}%".format(summary['bed_utilization_percent']))
        
        print("\n" + "="*80)
    
    def save_to_json(self, filename: str):
        """Guarda las estadísticas a un archivo JSON."""
        summary = self.get_summary()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Estadísticas guardadas en: {filename}")
