from flask import Flask, render_template, jsonify, request
import ee
import geemap
from datetime import datetime
import ee
import folium
from folium import plugins

app = Flask("Flood Detection System")

# Initialize Earth Engine
try:
    ee.Authenticate()
    ee.Initialize(project='atu-fyp')
    print("Earth Engine initialized successfully")
except Exception as e:
    print(f"Failed to initialize Earth Engine: {str(e)}")
    raise

# Define city boundaries
CITY_BOUNDARIES = {
    "Cork": ee.Geometry.Rectangle([-8.570, 51.729, -7.959, 52.009]),
    "Dublin": ee.Geometry.Rectangle([-6.400, 53.300, -6.100, 53.400]),
    "Limerick": ee.Geometry.Rectangle([-8.700, 52.600, -8.500, 52.700]),
    "Sligo": ee.Geometry.Rectangle([-8.500, 54.200, -8.300, 54.300]),
    "Galway": ee.Geometry.Rectangle([-9.300, 53.200, -8.900, 53.350])
}
# Cork boundary data ////// To fix 4 variables only 
# Latlong top left and latlong bottom right 
long1 = -8.570156845611686
lat1 = 52.00904254772663
long2 = -7.959042343658562
lat2 = 51.7292195887807

#Galway
#long1 = -9.5
#lat1 = 53
#long2 = -9
#lat2 = 54

CORK_AOI = ee.Geometry.Polygon([
    [long1, lat1],# top left 
    [long1, lat2],# bottom left
    [long2, lat2],# bottom right
    [long2, lat1] # top right
]).buffer(1000)  # 5km buffer

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze_flood', methods=['POST'])
def analyze_flood():
    try:
        # Get city or coordinates from request
        city = request.json.get('city')
        lat = request.json.get('latitude')
        lng = request.json.get('longitude')

        if city:
            if city not in CITY_BOUNDARIES:
                return jsonify({'success': False, 'error': f"City '{city}' is not supported."}), 400
            aoi = CITY_BOUNDARIES[city]
        elif lat and lng:
            # Create AOI from latitude and longitude
            aoi = ee.Geometry.Point([lng, lat]).buffer(5000)  # 5km buffer
        else:
            return jsonify({'success': False, 'error': 'No valid city or coordinates provided.'}), 400

        # Calculate date range (10 years ago)
        current_year = datetime.now().year
        analysis_year = current_year - 10
        flood_year = 2013  # Known flood year for Cork

        # Define data  (October)
        pre_flood_start = f'{analysis_year}-10-01'
        pre_flood_end = f'{analysis_year}-10-17'
        post_flood_start = f'{analysis_year}-10-18'
        post_flood_end = f'{analysis_year}-10-25'

        # Get Sentinel-1 data
        pre_flood = ee.ImageCollection('COPERNICUS/S1_GRD') \
            .filterBounds(aoi) \
            .filterDate(pre_flood_start, pre_flood_end) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
            .filter(ee.Filter.eq('instrumentMode', 'IW')) \
            .select('VV') \
            .median()

        post_flood = ee.ImageCollection('COPERNICUS/S1_GRD') \
            .filterBounds(aoi) \
            .filterDate(post_flood_start, post_flood_end) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
            .filter(ee.Filter.eq('instrumentMode', 'IW')) \
            .select('VV') \
            .median()

        # Calculate flood mask
        difference = post_flood.subtract(pre_flood)
        flood_mask = difference.gt(2).updateMask(difference.gt(2)).clip(aoi)


        # Calculate flood stats
        stats = flood_mask.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=aoi,
            scale=30,
            maxPixels=1e10
        ).getInfo()

        flood_percentage = round(stats['VV'] * 100, 2)
        was_flooded = flood_percentage > 5  # 5% threshold

        # Get map tiles for the clipped flood mask
        flood_tiles = flood_mask.getMapId({
            'min': 0, 
            'max': 1, 
            'palette': ['white', 'red']
        })

        # Get map tiles for the AOI boundary
        aoi_tiles = ee.Image().paint(aoi, 1, 3).getMapId({
            'palette': ['blue']
        })

        return jsonify({
            'success': True,
            'city': city,
            'latitude': lat,
            'longitude': lng,
            'year': analysis_year,
            'flood_percentage': flood_percentage,
            'was_flooded': 'YES' if was_flooded else 'NO',
            'map_tiles': {
                'flood': flood_tiles['tile_fetcher'].url_format,
                'aoi': aoi_tiles['tile_fetcher'].url_format
            },
            'aoi': aoi.getInfo(),
            'historical_note': f"Major floods occurred in {flood_year}" if analysis_year == flood_year else ""
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)