from flask import Flask, render_template, jsonify, request
import ee
import geemap
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/flood_history')
def flood_history():
    city = request.args.get('city', 'Cork')
    if city not in CITY_BOUNDARIES:
        return "City not supported", 400

    aoi = CITY_BOUNDARIES[city]

    # Calculate date range (10 years ago)
    current_year = datetime.now().year
    analysis_year = current_year - 10
    flood_year = 2013  # Known flood year for Cork

    # Define seasonal range (October, when floods typically occur)
    pre_flood_start = f'{analysis_year}-10-01'
    pre_flood_end = f'{analysis_year}-10-17'
    post_flood_start = f'{analysis_year}-10-18'
    post_flood_end = f'{analysis_year}-10-25'

    # Load Sentinel-1 data
    pre_flood_image = ee.ImageCollection('COPERNICUS/S1_GRD') \
        .filterBounds(aoi) \
        .filterDate(pre_flood_start, pre_flood_end) \
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
        .filter(ee.Filter.eq('instrumentMode', 'IW')) \
        .select('VV') \
        .median()

    post_flood_image = ee.ImageCollection('COPERNICUS/S1_GRD') \
        .filterBounds(aoi) \
        .filterDate(post_flood_start, post_flood_end) \
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
        .filter(ee.Filter.eq('instrumentMode', 'IW')) \
        .select('VV') \
        .median()

    # Calculate difference and flood mask
    difference_image = post_flood_image.subtract(pre_flood_image)
    flood_mask = difference_image.gt(2)  # Threshold = 2

    # Calculate flood statistics
    stats = flood_mask.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=aoi,
        scale=30,
        maxPixels=1e10
    ).getInfo()

    flood_percentage = round(stats['VV'] * 100, 2)
    was_flooded = "YES" if flood_percentage > 5 else "NO"  # 5% threshold for flood determination

    # Get map tiles
    flood_tiles = flood_mask.getMapId({'min': 0, 'max': 1, 'palette': ['white', 'red']})
    aoi_tiles = ee.Image().paint(aoi, 1, 3).getMapId({'palette': ['blue']})

    return render_template('flood_history.html', 
                           city=city, 
                           year=analysis_year, 
                           flood_percentage=flood_percentage, 
                           was_flooded=was_flooded, 
                           map_tiles={'flood': flood_tiles['tile_fetcher'].url_format, 'aoi': aoi_tiles['tile_fetcher'].url_format}, 
                           aoi=aoi.getInfo(), 
                           historical_note=f"Major floods occurred in {flood_year}" if analysis_year == flood_year else "")

if __name__ == '__main__':
    app.run(debug=True)