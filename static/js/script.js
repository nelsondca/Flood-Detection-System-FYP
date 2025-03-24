document.getElementById('detect-flood').addEventListener('click', () => {
    const city = 'Cork';
    const preFloodStart = '2023-10-15';
    const preFloodEnd = '2023-10-17';
    const postFloodStart = '2023-10-18';
    const postFloodEnd = '2023-10-25';

    fetch(`/detect_flood?city=${city}&pre_flood_start=${preFloodStart}&pre_flood_end=${preFloodEnd}&post_flood_start=${postFloodStart}&post_flood_end=${postFloodEnd}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Flood detection completed! Check the map.');
                // Load the generated map (simplified example)
                const floodLayer = L.tileLayer(data.map_url).addTo(map);
            } else {
                alert('Flood detection failed. Please try again.');
            }
        });
});

// Initialize map centered on Cork
const map = L.map('map').setView([51.8969, -8.4863], 11);

// Add base map layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);