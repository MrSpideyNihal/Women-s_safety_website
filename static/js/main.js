document.addEventListener('DOMContentLoaded', () => {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Update user location periodically if logged in
    if (document.getElementById('emergencyBtn')) {
        setInterval(() => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const { latitude, longitude } = position.coords;
                        // You could send this to the server to update user location
                        // fetch('/update-location', {
                        //     method: 'POST',
                        //     headers: { 'Content-Type': 'application/json' },
                        //     body: JSON.stringify({ lat: latitude, lng: longitude })
                        // });
                    }
                );
            }
        }, 60000); // Update every minute
    }
});
fetch('/api/alerts')
  .then(response => response.json())
  .then(data => {
      let alertContainer = document.getElementById('alert-list');
      alertContainer.innerHTML = "";
      data.forEach(alert => {
          alertContainer.innerHTML += `<li class="alert-card"><strong>${alert.title}</strong> - ${alert.description} <br><small>${alert.timestamp}</small></li>`;
      });
  });

