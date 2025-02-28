let map;
let userMarker;
let emergencyMarkers = [];

function initMap() {
    map = L.map('map').setView([0, 0], 13);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Try to get user's location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                map.setView([latitude, longitude], 13);
                
                if (userMarker) {
                    userMarker.setLatLng([latitude, longitude]);
                } else {
                    userMarker = L.marker([latitude, longitude]).addTo(map);
                }
            },
            (error) => {
                console.error('Error getting location:', error);
            }
        );
    }
}

function addEmergencyMarker(lat, lng) {
    const emergencyIcon = L.divIcon({
        className: 'emergency-icon',
        html: '<div style="background-color: #FF5252; width: 20px; height: 20px; border-radius: 50%;"></div>'
    });

    const marker = L.marker([lat, lng], { icon: emergencyIcon }).addTo(map);
    emergencyMarkers.push(marker);
}

document.addEventListener('DOMContentLoaded', () => {
    initMap();

    const emergencyBtn = document.getElementById('emergencyBtn');
    const emergencyForm = document.getElementById('emergencyForm');
    
    if (emergencyBtn && emergencyForm) {
        emergencyBtn.addEventListener('click', () => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const { latitude, longitude } = position.coords;
                        document.getElementById('emergencyLat').value = latitude;
                        document.getElementById('emergencyLng').value = longitude;
                        emergencyForm.submit();
                    },
                    (error) => {
                        console.error('Error getting location:', error);
                        alert('Unable to get your location. Please try again.');
                    }
                );
            }
        });
    }
});
