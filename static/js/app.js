// Variables globales
let patientChart = null;
let utilizationChart = null;
let currentResults = null;

// Ejecutar simulación
async function runSimulation() {
    const btn = document.getElementById('runSimulationBtn');
    const spinner = document.getElementById('loadingSpinner');
    const resultsSection = document.getElementById('resultsSection');
    
    // Deshabilitar botón y mostrar loading
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Ejecutando...';
    spinner.style.display = 'block';
    resultsSection.style.display = 'none';
    
    try {
        const response = await fetch('/api/run-simulation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            currentResults = data.data;
            displayResults(data.data);
            resultsSection.style.display = 'block';
            showSuccessNotification('Simulación completada exitosamente');
        } else {
            showErrorNotification(data.message || 'Error en la simulación');
        }
    } catch (error) {
        console.error('Error:', error);
        showErrorNotification('Error al ejecutar la simulación: ' + error.message);
    } finally {
        // Reabilitar botón
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-play-circle"></i> Ejecutar Simulación';
        spinner.style.display = 'none';
    }
}

// Mostrar resultados
function displayResults(results) {
    // Estadísticas generales
    document.getElementById('patientsServed').textContent = results.patients_served;
    document.getElementById('patientsAbandoned').textContent = results.patients_abandoned;
    document.getElementById('servedPercentage').textContent = results.served_percentage.toFixed(2) + '%';
    document.getElementById('totalPatients').textContent = results.total_patients;
    
    // Tiempos de espera
    const waitTimes = results.average_waiting_time_by_priority;
    document.getElementById('waitEmergency').textContent = waitTimes.EMERGENCY.toFixed(2);
    document.getElementById('waitUrgency').textContent = waitTimes.URGENCY.toFixed(2);
    document.getElementById('waitConsultation').textContent = waitTimes.CONSULTATION.toFixed(2);
    
    // Utilización de recursos
    const doctorUtil = results.doctor_utilization_percent;
    const nurseUtil = results.nurse_utilization_percent;
    const bedUtil = results.bed_utilization_percent;
    
    document.getElementById('doctorUtilization').textContent = doctorUtil.toFixed(2) + '%';
    document.getElementById('doctorBar').style.width = Math.min(100, doctorUtil) + '%';
    
    document.getElementById('nurseUtilization').textContent = nurseUtil.toFixed(2) + '%';
    document.getElementById('nurseBar').style.width = Math.min(100, nurseUtil) + '%';
    
    document.getElementById('bedUtilization').textContent = bedUtil.toFixed(2) + '%';
    document.getElementById('bedBar').style.width = Math.min(100, bedUtil) + '%';
    
    // Gráficos
    updatePatientChart(results);
    updateUtilizationChart(results);
}

// Gráfico de distribución de pacientes
function updatePatientChart(results) {
    const ctx = document.getElementById('patientChart').getContext('2d');
    
    if (patientChart) {
        patientChart.destroy();
    }
    
    patientChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Atendidos', 'Abandonados'],
            datasets: [{
                data: [results.patients_served, results.patients_abandoned],
                backgroundColor: [
                    '#27ae60',  // Verde para atendidos
                    '#e74c3c'   // Rojo para abandonados
                ],
                borderColor: ['#229954', '#c0392b'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.parsed + ' pacientes';
                        }
                    }
                }
            }
        }
    });
}

// Gráfico de utilización de recursos
function updateUtilizationChart(results) {
    const ctx = document.getElementById('utilizationChart').getContext('2d');
    
    if (utilizationChart) {
        utilizationChart.destroy();
    }
    
    utilizationChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Médicos', 'Enfermeras', 'Camas'],
            datasets: [{
                label: 'Utilización (%)',
                data: [
                    results.doctor_utilization_percent,
                    results.nurse_utilization_percent,
                    results.bed_utilization_percent
                ],
                backgroundColor: [
                    '#3498db',  // Azul
                    '#9b59b6',  // Púrpura
                    '#f39c12'   // Naranja
                ],
                borderColor: ['#2980b9', '#8e44ad', '#e67e22'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// Descargar JSON
function downloadJSON() {
    if (!currentResults) {
        showErrorNotification('No hay resultados para descargar');
        return;
    }
    
    const dataStr = JSON.stringify(currentResults, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `resultados_simulacion_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
}

// Imprimir reporte
function printReport() {
    window.print();
}

// Notificaciones
function showSuccessNotification(message) {
    showNotification(message, 'success');
}

function showErrorNotification(message) {
    showNotification(message, 'danger');
}

function showNotification(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.insertAdjacentElement('beforebegin', alertDiv);
    
    // Auto-cerrar después de 5 segundos
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Verificar que el servidor está activo
async function checkServerHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('Servidor activo:', data);
    } catch (error) {
        console.error('Error conectando al servidor:', error);
    }
}

// Cargar configuración
async function loadConfiguration() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();
        console.log('Configuración:', config);
    } catch (error) {
        console.error('Error cargando configuración:', error);
    }
}

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard cargado');
    checkServerHealth();
    loadConfiguration();
});
