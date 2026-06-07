function confirmDelete() {
    return window.confirm("Delete this customer and related records?");
}

function renderRevenueChart() {
    const canvas = document.getElementById("revenueChart");
    if (!canvas || !window.Chart) {
        return;
    }

    new Chart(canvas, {
        type: "line",
        data: {
            labels: window.revenueLabels || [],
            datasets: [{
                label: "Revenue",
                data: window.revenueValues || [],
                borderColor: "#1d6ee8",
                backgroundColor: "rgba(29, 110, 232, 0.12)",
                fill: true,
                tension: 0.35
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}
