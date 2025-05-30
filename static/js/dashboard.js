$(document).ready(function() {
    // Cargar Métricas para las Tarjetas
    $.ajax({
        url: '/api/metricas',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            $('#mes-top').text(data.mes_top || 'N/A');
            $('#reservas-mes-top').text(`${data.reservas_mes_top} reservas`);
            $('#total-facturado').text(`$${data.total_facturado.toFixed(2)}`);
            $('#total-reservas').text(data.total_reservas);
            $('#clientes-activos').text(data.clientes_activos);
        },
        error: function() {
            console.error('Error al cargar métricas');
            $('#mes-top').text('Error');
            $('#reservas-mes-top').text('Error');
            $('#total-facturado').text('Error');
            $('#total-reservas').text('Error');
            $('#clientes-activos').text('Error');
        }
    });

    // Reservas por Mes
    $.ajax({
        url: '/api/reservas_por_mes',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            const labels = data.map(item => item.mes);
            const values = data.map(item => item.total);
            new Chart(document.getElementById('reservasPorMes'), {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Reservas por Mes',
                        data: values,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, title: { display: true, text: 'Número de Reservas' } },
                        x: { title: { display: true, text: 'Mes' } }
                    }
                }
            });
        },
        error: function() {
            console.error('Error al cargar reservas por mes');
        }
    });

    // Reservas por Habitación
    $.ajax({
        url: '/api/reservas_por_habitacion',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            const labels = data.map(item => item.habitacion);
            const values = data.map(item => item.total);
            new Chart(document.getElementById('reservasPorHabitacion'), {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Reservas por Habitación',
                        data: values,
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, title: { display: true, text: 'Número de Reservas' } },
                        x: { title: { display: true, text: 'Habitación' } }
                    }
                }
            });
        },
        error: function() {
            console.error('Error al cargar reservas por habitación');
        }
    });

    // Pagos por Método
    $.ajax({
        url: '/api/pagos_por_metodo',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            new Chart(document.getElementById('pagosPorMetodo'), {
                type: 'pie',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Pagos por Método',
                        data: data.data,
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.5)',
                            'rgba(153, 102, 255, 0.5)',
                            'rgba(255, 159, 64, 0.5)',
                            'rgba(128, 128, 128, 0.5)' // Color para "Sin Clasificar"
                        ],
                        borderColor: [
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)',
                            'rgba(128, 128, 128, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' },
                        title: { display: true, text: 'Distribución de Pagos por Método' }
                    }
                }
            });
        },
        error: function() {
            console.error('Error al cargar pagos por método');
        }
    });

    // Facturas por Mes
    $.ajax({
        url: '/api/facturas_por_mes',
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            const labels = data.map(item => item.mes);
            const values = data.map(item => item.total);
            new Chart(document.getElementById('facturasPorMes'), {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Monto de Facturas por Mes',
                        data: values,
                        fill: false,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, title: { display: true, text: 'Monto Total ($)' } },
                        x: { title: { display: true, text: 'Mes' } }
                    }
                }
            });
        },
        error: function() {
            console.error('Error al cargar facturas por mes');
        }
    });
});