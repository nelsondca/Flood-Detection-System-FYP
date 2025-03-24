from flask import Flask, render_template, jsonify, request
import ee
import geemap
from datetime import datetime

app = Flask(__name__)

# Initialize Earth Engine
try:
    ee.Authenticate()
    ee.Initialize(project='atu-fyp')
    print("Earth Engine initialized successfully")
except Exception as e:
    print(f"Failed to initialize Earth Engine: {str(e)}")
    raise

# Cork boundary data
CORK_AOI = ee.Geometry.Polygon([
    [-8.570156845611686, 52.00904254772663],
    [-8.570156845611686, 51.7292195887807],
    [-7.959042343658562, 51.7292195887807],
    [-7.959042343658562, 52.00904254772663]
]).buffer(5000)  # 5km buffer

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze_flood', methods=['POST'])
def analyze_flood():
    try:
        # Hardcode Cork analysis since it's our only city
        current_year = datetime.now().year
        analysis_year = current_year - 10  # 10 years ago
        flood_year = 2013  # Known flood year for Cork

        # Define date ranges (October)
        pre_flood_start = f'{analysis_year}-10-01'
        pre_flood_end = f'{analysis_year}-10-17'
        post_flood_start = f'{analysis_year}-10-18'
        post_flood_end = f'{analysis_year}-10-25'

        # Get Sentinel-1 data
        pre_flood = ee.ImageCollection('COPERNICUS/S1_GRD') \
            .filterBounds(CORK_AOI) \
            .filterDate(pre_flood_start, pre_flood_end) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
            .filter(ee.Filter.eq('instrumentMode', 'IW')) \
            .select('VV') \
            .median()

        post_flood = ee.ImageCollection('COPERNICUS/S1_GRD') \
            .filterBounds(CORK_AOI) \
            .filterDate(post_flood_start, post_flood_end) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
            .filter(ee.Filter.eq('instrumentMode', 'IW')) \
            .select('VV') \
            .median()

        # Calculate flood mask
        difference = post_flood.subtract(pre_flood)
        flood_mask = difference.gt(2)  # Threshold of 2 dB

        # Calculate flood stats
        stats = flood_mask.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=CORK_AOI,
            scale=30,
            maxPixels=1e10
        ).getInfo()

        flood_percentage = round(stats['VV'] * 100, 2)
        was_flooded = flood_percentage > 5  # 5% threshold

        # Get map tiles
        flood_tiles = flood_mask.getMapId({
            'min': 0, 
            'max': 1, 
            'palette': ['white', 'red']
        })
        
        aoi_tiles = ee.Image().paint(CORK_AOI, 1, 3).getMapId({
            'palette': ['blue']
        })

        return jsonify({
            'success': True,
            'city': 'Cork, Ireland',
            'year': analysis_year,
            'flood_percentage': flood_percentage,
            'was_flooded': 'YES' if was_flooded else 'NO',
            'map_tiles': {
                'flood': flood_tiles['tile_fetcher'].url_format,
                'aoi': aoi_tiles['tile_fetcher'].url_format
            },
            'aoi': CORK_AOI.getInfo(),
            'historical_note': f"Major floods occurred in {flood_year}" if analysis_year == flood_year else ""
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)