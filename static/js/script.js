// Initialize map
const map = L.map('map').setView([51.8969, -8.4863], 10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Store flood and AOI layers globally
const layers = {
    flood: null,
    aoi: null
};

// Find Location Button (Eircode lookup)
document.getElementById('find-location').addEventListener('click', async () => {
    const eircode = document.getElementById('eircode-input').value.trim();
    if (!eircode) {
        alert('Please enter a valid Eircode.');
        return;
    }

    const apiKey = 'AIzaSyArXKNwEr-9tUzn_gylqKtGGrK4aKUcWng'; 
    const geocodeUrl = `https://maps.googleapis.com/maps/api/geocode/json?address=${eircode}&key=${apiKey}`;

    try {
        document.getElementById('loading').style.display = 'block';
        const response = await fetch(geocodeUrl);
        if (!response.ok) {
            throw new Error(`Geocoding API error: ${response.status}`);
        }

        const data = await response.json();
        if (data.status !== 'OK') {
            throw new Error(`Geocoding failed: ${data.status}`);
        }

        const location = data.results[0].geometry.location;
        const lat = location.lat;
        const lng = location.lng;

        document.getElementById('location-result').innerText = `Latitude: ${lat}, Longitude: ${lng}`;

        map.setView([lat, lng], 12);
    } catch (error) {
        alert('Failed to find location: ' + error.message);
        console.error('Error:', error);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
});

// Check Flood History Button
document.getElementById('check-flood-history').addEventListener('click', async () => {
    const city = document.getElementById('city-select').value;

    try {
        document.getElementById('loading').style.display = 'block';
        const response = await fetch('/analyze_flood', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ city })
        });

        const data = await response.json();
        if (data.success) {
            document.getElementById('result-city').innerText = data.city;
            document.getElementById('result-year').innerText = data.year;
            document.getElementById('result-percentage').innerText = data.flood_percentage;
            document.getElementById('result-flooded').innerText = data.was_flooded;
            document.getElementById('historical-note').innerText = data.historical_note;

            // Remove previous layers if any
            Object.values(layers).forEach(layer => {
                if (layer) {
                    map.removeLayer(layer);
                }
            });

            // Add flood layer 
            layers.flood = L.tileLayer(data.map_tiles.flood, { opacity: 0.7 }).addTo(map);

            // Add AOI layer
            layers.aoi = L.tileLayer(data.map_tiles.aoi, { opacity: 0.5 }).addTo(map);

            // Zoom to AOI
            const aoiLayer = L.geoJSON(data.aoi);
            map.fitBounds(aoiLayer.getBounds());

            document.getElementById('results').style.display = 'block';
        } else {
            alert('Error: ' + (data.error || 'Unknown error occurred'));
        }
    } catch (error) {
        alert('Failed to analyze flood: ' + error.message);
        console.error('Error:', error);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
});
