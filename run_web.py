#!/usr/bin/env python3
"""
Script para ejecutar la aplicación web del simulador hospitalario.
Inicia el servidor Flask con la interfaz web.

Uso: python run_web.py
"""

import os
import sys
import webbrowser
import time
from threading import Thread

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def open_browser():
    """Abre el navegador automáticamente después de que inicia el servidor."""
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:5000')
        print("✅ Navegador abierto automáticamente")
    except:
        print("⚠️  No se pudo abrir el navegador automáticamente")
        print("   Por favor, abre manualmente: http://localhost:5000")

if __name__ == '__main__':
    print("\n" + "="*80)
    print("SERVIDOR WEB - SIMULACIÓN DEL SISTEMA HOSPITALARIO")
    print("="*80)
    
    # Verificar que Flask está instalado
    try:
        from app import app
    except ImportError:
        print("❌ Error: Flask no está instalado")
        print("   Ejecuta: pip install -r requirements.txt")
        sys.exit(1)
    
    # Crear thread para abrir el navegador
    browser_thread = Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print("\n📊 Iniciando aplicación web...")
    print("🌐 URL: http://localhost:5000")
    print("📱 Abre esta URL en tu navegador")
    print("\n✨ El docente puede acceder desde cualquier navegador")
    print("   en la misma red usando la dirección IP del servidor\n")
    print("Presiona CTRL+C para detener el servidor\n")
    print("="*80 + "\n")
    
    # Iniciar servidor Flask
    app.run(debug=False, host='0.0.0.0', port=5000)
