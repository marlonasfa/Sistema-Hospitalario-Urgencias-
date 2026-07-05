#!/usr/bin/env python3
"""
Script principal para ejecutar la simulación del hospital.
Simulador de Sistema Hospitalario de Urgencias
Universidad Privada San Juan Bautista - Ingeniería de Sistemas
"""

import os
import sys
from datetime import datetime

# Asegurar que el directorio results existe
os.makedirs('results', exist_ok=True)

from src.hospital_simulation import run_simulation


def main():
    """Función principal."""
    print("\n" + "="*80)
    print("SIMULACIÓN DEL SISTEMA HOSPITALARIO DE URGENCIAS")
    print("Universidad Privada San Juan Bautista - 2026-I")
    print("Asignatura: Optimización y Simulación de Sistemas")
    print("="*80 + "\n")
    
    # Ejecutar simulación
    hospital = run_simulation()
    
    # Guardar estadísticas
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f'results/estadisticas_{timestamp}.json'
    hospital.stats.save_to_json(json_filename)
    
    # Guardar logs
    log_filename = f'results/logs_{timestamp}.txt'
    with open(log_filename, 'w', encoding='utf-8') as f:
        for log in hospital.logs:
            f.write(log + '\n')
    
    print(f"\n✅ Logs guardados en: {log_filename}")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
