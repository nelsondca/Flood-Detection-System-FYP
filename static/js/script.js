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
const map = L.map('map').setView([51.8969, -8.4863], 10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Find Location Button
document.getElementById('find-location').addEventListener('click', async () => {
    const eircode = document.getElementById('eircode-input').value.trim();
    if (!eircode) {
        alert('Please enter a valid Eircode.');
        return;
    }

    const apiKey = 'AIzaSyArXKNwEr-9tUzn_gylqKtGGrK4aKUcWng'; // API key
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

        // Display the location result
        document.getElementById('location-result').innerText = `Latitude: ${lat}, Longitude: ${lng}`;

        // Center the map on the found location
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

            // Add AOI boundary to the map
            const aoiLayer = L.geoJSON(data.aoi);
            map.fitBounds(aoiLayer.getBounds());
            aoiLayer.addTo(map);

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