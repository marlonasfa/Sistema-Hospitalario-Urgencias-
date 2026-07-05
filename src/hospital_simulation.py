"""
Simulador de Sistema Hospitalario de Urgencias usando SimPy.
Universidad Privada San Juan Bautista - Ingeniería de Sistemas
Optimización y Simulación de Sistemas - 2026-I
"""

import simpy
import random
from typing import List
import sys
import os

# Añadir rutas al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import (
    SIMULATION_TIME, NUM_DOCTORS, NUM_NURSES, NUM_BEDS, 
    ARRIVAL_RATES, SERVICE_TIMES, MAX_WAITING_TIME, 
    PRIORITY, RANDOM_SEED, REPORT_INTERVAL
)
from src.patient import Patient
from src.statistics import StatisticsCollector


class HospitalEmergencySystem:
    """Sistema de emergencias hospitalario con SimPy."""
    
    def __init__(self):
        """Inicializa el sistema hospitalario."""
        self.env = simpy.Environment()
        
        # Recursos
        self.doctors = simpy.PriorityResource(self.env, NUM_DOCTORS)
        self.nurses = simpy.PriorityResource(self.env, NUM_NURSES)
        self.beds = simpy.PriorityResource(self.env, NUM_BEDS)
        
        # Contador de pacientes
        self.patient_counter = 0
        
        # Recolector de estadísticas
        self.stats = StatisticsCollector()
        
        # Logs para seguimiento
        self.logs = []
    
    def get_next_patient_id(self) -> int:
        """Obtiene el siguiente ID para un paciente."""
        self.patient_counter += 1
        return self.patient_counter
    
    def patient_arrival_generator(self):
        """Genera llegadas aleatorias de pacientes."""
        while True:
            # Decidir tipo de paciente basado en tasas de llegada
            arrival_random = random.random()
            cumulative = 0
            
            for priority_type, rate in ARRIVAL_RATES.items():
                cumulative += rate
                if arrival_random < cumulative / sum(ARRIVAL_RATES.values()):
                    break
            
            # Crear paciente
            patient = Patient(
                id=self.get_next_patient_id(),
                priority_type=priority_type,
                arrival_time=self.env.now,
                priority_level=PRIORITY[priority_type],
                service_time=random.gauss(
                    SERVICE_TIMES[priority_type]['mean'],
                    SERVICE_TIMES[priority_type]['std']
                )
            )
            
            # Asegurar tiempo de servicio positivo
            patient.service_time = max(1, patient.service_time)
            
            # Procesar el paciente
            self.env.process(self.patient_process(patient))
            
            # Siguiente llegada
            inter_arrival_time = random.expovariate(1.0 / 3.0)  # 3 minutos promedio
            yield self.env.timeout(inter_arrival_time)
    
    def patient_process(self, patient: Patient):
        """Proceso de un paciente en el hospital."""
        patient.start_wait_time = self.env.now
        
        # Registrar llegada
        self.logs.append(f"[{self.env.now:.2f} min] Paciente #{patient.id:04d} "
                        f"({patient.get_priority_name()}) llegó")
        
        # Intenta obtener una cama
        try:
            # Esperar con timeout si es necesario
            max_wait = MAX_WAITING_TIME[patient.priority_type]
            
            # Crear un evento de timeout
            timeout_event = self.env.timeout(max_wait)
            bed_request = self.beds.request(priority=patient.priority_level)
            
            # Raza entre timeout y obtención de cama
            results = yield bed_request | timeout_event
            
            # Verificar si obtuvo la cama o si expiró el timeout
            if timeout_event not in results or bed_request.triggered:
                if not bed_request.triggered:
                    # Timeout ocurrió, paciente abandona
                    patient.abandoned = True
                    patient.abandon_time = self.env.now
                    self.stats.add_abandoned_patient(patient)
                    self.logs.append(f"[{self.env.now:.2f} min] Paciente #{patient.id:04d} "
                                   f"({patient.get_priority_name()}) ABANDONÓ (timeout de espera)")
                    return
                
                # Obtuvo la cama
                patient.start_service_time = self.env.now
                patient.waiting_time = patient.start_service_time - patient.start_wait_time
                
                self.logs.append(f"[{self.env.now:.2f} min] Paciente #{patient.id:04d} "
                               f"({patient.get_priority_name()}) obtuvo cama "
                               f"(esperó {patient.waiting_time:.2f} min)")
                
                try:
                    # Solicitar doctor
                    with self.doctors.request(priority=patient.priority_level) as doctor_req:
                        yield doctor_req
                        
                        # Registrar uso de doctor
                        self.stats.record_doctor_usage(
                            self.env.now,
                            self.doctors.users.__len__(),
                            NUM_DOCTORS
                        )
                        
                        # Solicitar enfermera
                        with self.nurses.request(priority=patient.priority_level) as nurse_req:
                            yield nurse_req
                            
                            # Registrar uso de enfermera
                            self.stats.record_nurse_usage(
                                self.env.now,
                                self.nurses.users.__len__(),
                                NUM_NURSES
                            )
                            
                            # Registrar uso de cama
                            self.stats.record_bed_usage(
                                self.env.now,
                                self.beds.users.__len__(),
                                NUM_BEDS
                            )
                            
                            # Atender al paciente
                            self.logs.append(f"[{self.env.now:.2f} min] Paciente #{patient.id:04d} "
                                           f"comenzó atención")
                            
                            yield self.env.timeout(patient.service_time)
                            
                            patient.end_service_time = self.env.now
                            patient.served = True
                            patient.total_time_in_system = patient.end_service_time - patient.arrival_time
                            
                            self.stats.add_served_patient(patient)
                            self.logs.append(f"[{self.env.now:.2f} min] Paciente #{patient.id:04d} "
                                           f"ATENDIDO ✓")
                finally:
                    self.beds.release(bed_request)
        
        except simpy.Interrupt:
            patient.abandoned = True
            patient.abandon_time = self.env.now
            self.stats.add_abandoned_patient(patient)
            self.logs.append(f"[{self.env.now:.2f} min] Paciente #{patient.id:04d} "
                           f"fue interrumpido")
    
    def resource_monitor(self):
        """Monitorea el uso de recursos periódicamente."""
        while True:
            # Registrar estado actual
            self.stats.record_doctor_usage(
                self.env.now,
                len(self.doctors.users),
                NUM_DOCTORS
            )
            self.stats.record_nurse_usage(
                self.env.now,
                len(self.nurses.users),
                NUM_NURSES
            )
            self.stats.record_bed_usage(
                self.env.now,
                len(self.beds.users),
                NUM_BEDS
            )
            
            yield self.env.timeout(REPORT_INTERVAL)
    
    def run(self):
        """Ejecuta la simulación."""
        print("🏥 Iniciando simulación del Sistema Hospitalario de Urgencias...")
        print(f"   Duración: {SIMULATION_TIME} minutos")
        print(f"   Recursos: {NUM_DOCTORS} médicos, {NUM_NURSES} enfermeras, {NUM_BEDS} camas")
        print()
        
        # Iniciar generadores
        self.env.process(self.patient_arrival_generator())
        self.env.process(self.resource_monitor())
        
        # Ejecutar simulación
        self.env.run(until=SIMULATION_TIME)
        
        print("\n✅ Simulación completada")
    
    def print_logs(self, last_n: int = None):
        """Imprime los logs de la simulación."""
        logs_to_print = self.logs[-last_n:] if last_n else self.logs
        
        print("\n📋 LOGS DE LA SIMULACIÓN (últimos {} eventos):".format(
            len(logs_to_print)))
        print("-" * 80)
        for log in logs_to_print:
            print(log)
        print("-" * 80)


def run_simulation():
    """Función principal para ejecutar la simulación."""
    # Configurar semilla aleatoria
    random.seed(RANDOM_SEED)
    
    # Crear y ejecutar simulación
    hospital = HospitalEmergencySystem()
    hospital.run()
    
    # Mostrar estadísticas
    hospital.stats.print_report()
    
    # Mostrar últimos logs
    hospital.print_logs(last_n=20)
    
    return hospital


if __name__ == "__main__":
    run_simulation()
