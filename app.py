"""
Aplicación web Flask para visualizar la simulación hospitalaria.
Permite ejecutar simulaciones y ver resultados en tiempo real.
Universidad Privada San Juan Bautista - Ingeniería de Sistemas
"""

from flask import Flask, render_template, jsonify, request, send_file
from datetime import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.hospital_simulation import HospitalEmergencySystem
from config.settings import SIMULATION_TIME

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Variables globales para almacenar el estado
current_simulation = None
simulation_results = None


@app.route('/')
def index():
    """Página principal."""
    return render_template('index.html')


@app.route('/api/run-simulation', methods=['POST'])
def run_simulation():
    """Ejecuta una simulación y retorna los resultados."""
    global current_simulation, simulation_results
    
    try:
        # Ejecutar simulación
        current_simulation = HospitalEmergencySystem()
        current_simulation.run()
        
        # Obtener resultados
        simulation_results = current_simulation.stats.get_summary()
        
        # Agregar información adicional
        simulation_results['timestamp'] = datetime.now().isoformat()
        simulation_results['simulation_logs'] = current_simulation.logs[:30]  # Primeros 30 logs
        
        return jsonify({
            'status': 'success',
            'data': simulation_results
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/results', methods=['GET'])
def get_results():
    """Retorna los resultados de la última simulación."""
    if simulation_results is None:
        return jsonify({
            'status': 'error',
            'message': 'No hay simulación disponible'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': simulation_results
    }), 200


@app.route('/api/export-json', methods=['GET'])
def export_json():
    """Descarga los resultados en JSON."""
    if simulation_results is None:
        return jsonify({'error': 'No data available'}), 404
    
    # Crear archivo temporal
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'resultados_simulacion_{timestamp}.json'
    
    return jsonify(simulation_results), 200, {
        'Content-Disposition': f'attachment; filename={filename}',
        'Content-Type': 'application/json'
    }


@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar que el servidor está activo."""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'simulation_time': SIMULATION_TIME
    }), 200


@app.route('/api/config', methods=['GET'])
def get_config():
    """Obtener configuración actual de la simulación."""
    from config.settings import (
        SIMULATION_TIME, NUM_DOCTORS, NUM_NURSES, NUM_BEDS,
        ARRIVAL_RATES, SERVICE_TIMES, MAX_WAITING_TIME
    )
    
    return jsonify({
        'simulation_time': SIMULATION_TIME,
        'resources': {
            'doctors': NUM_DOCTORS,
            'nurses': NUM_NURSES,
            'beds': NUM_BEDS
        },
        'arrival_rates': ARRIVAL_RATES,
        'service_times': SERVICE_TIMES,
        'max_waiting_time': MAX_WAITING_TIME
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Manejo de rutas no encontradas."""
    return jsonify({'error': 'Ruta no encontrada'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores internos."""
    return jsonify({'error': 'Error interno del servidor'}), 500


if __name__ == '__main__':
    print("\n" + "="*80)
    print("SERVIDOR WEB - SIMULACIÓN HOSPITALARIA")
    print("="*80)
    print("\n✅ Servidor iniciado en: http://localhost:5000")
    print("📊 Dashboard disponible en: http://localhost:5000")
    print("\nPresiona CTRL+C para detener el servidor\n")
    print("="*80 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
