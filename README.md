# Flood-Detection-System-FYP using GOOGLE EARTH ENGINE ( Colour Change Analysis)

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Methodology](#methodology)
- [Validation](#validation)


## Project Overview
This project was developed as my Final Year Project, focusing on image-based flood detection using Google Earth Eangine satelite data and computer techniques. The system analyzes images to identify water levels and flood conditions.

The system combines:
- Google Earth Engine for satellite data processing
- Sentinel-1 SAR data for flood detection
- Sentinel-2 optical data for validation
- Flask web interface for visualization

The system focuses on Cork, Ireland as a case study area, which experienced significant flooding in October 2023.

## Key Features
- **Multi-sensor analysis**: Combines Sentinel-1 radar and Sentinel-2 optical data
- **Temporal comparison**: Pre-flood vs post-flood period analysis
- **Web dashboard**: Interactive visualization of results
- **Quantitative metrics**: Flood extent percentage and validation statistics
- **Geospatial processing**: Handles both city boundaries and custom coordinates

## Installation

### Prerequisites
- Python 3.6+
- Google Earth Engine account ( with API enabled)
- Google Cloud Poject


### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/nelsondca/Flood-Detection-System-FYP.git
   cd Flood-Detection-System-FYP

2. Set up Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Authenticate Earth Engine:
   ```bash
   earthengine authenticate

4. Set up environment variables:
   ```bash
   echo "GEE_PROJCT=atu-fyp" > .env
   echo "GEE_SERVICE_ACCOUNT

## How to run
(start the Flask server)
python app.py

Then access the web interface at:
http://localhost:5000

For development and testing:

Open GEEtest.ipynb 


Output

The script will:
    1- Display the processed area with the detection layers
    2- Percentage of flood risk or area flooded

## Project Structure

Flood-Detection-System-FYP/
├── static/                 # Web assets
│   ├── css/                # Stylesheets
│   └── js/                 # JavaScript
├── templates/              # HTML templates
│   ├── flood_history.html  # Historical data
│   └── index.html          # Main interface
├── GEEtest.ipynb           # Earth Engine analysis
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
└── README.md

## Methodology

1. Data Collection

Sentinel-1 SAR (C-band radar):

    VV polarization
    IW mode
    10m resolution

Sentinel-2 MSI (optical):

    B3 (Green) and B8 (NIR) for NDWI
    10m resolution

2. Flood Detection Algorithm

Define Area of Interest (Cork boundary)
Collect pre-flood (Oct 1-17) and post-flood (Oct 18-25) images
Calculate dB difference: post_flood - pre_flood
Apply threshold (>2dB) to create flood mask
Calculate flood percentage within AOI

3. Validation

Compare with Sentinel-2 NDWI (>0.3)

Calculate confusion matrix:
    True Positives (both methods detect flood)
    False Positives (SAR only)
    False Negatives (NDWI only)

Accuracy = TP / (TP + FP + FN)
Precision = TP / (TP + FP)
Recall = TP / (TP + FN)

## Technical Implementation