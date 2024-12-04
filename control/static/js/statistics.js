document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('departmentsChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: departmentsData.labels,
            datasets: [{
                label: 'Количество сотрудников',
                data: departmentsData.data,
                backgroundColor: 'rgba(60,141,188,0.8)',
                borderColor: 'rgba(60,141,188,1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });
});