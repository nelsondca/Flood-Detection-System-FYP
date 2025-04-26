# Flood Detection System

## Table of Contents
- [Project Description](#project-description)
- [Installation](#installation)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [How to Run](#how-to-run)
- [For Development and Testing (Running the Jupyter Notebook)](#for-development-and-testing-running-the-jupyter-notebook)
- [Example](#example)
- [Output](#output)
- [Technologies Used](#technologies-used)
- [Outputs](#outputs)
- [Future Work](#future-work)
- [Documentation/Research](#documentationresearch)

## Project Description
This project was developed as a Final Year Project, focusing on flood detection using satellite data and geospatial analysis.  
Google Earth Engine (GEE) is used for processing Sentinel-1 radar and Sentinel-2 optical data to detect and visualize flooded areas.

The system focuses on Cork, Ireland — a region that experienced record flooding in October 2023 — but it can be adapted to analyze any other area on the map.

It combines advanced geospatial processing with an intuitive web interface for visualization.

## Installation

> **Note:** To use this project, you must have your own Google Earth Engine account.  
> Sign up for free at [Google Earth Engine Signup](https://signup.earthengine.google.com/).

### Prerequisites
- Python 3.8+
- Google Earth Engine account (with API enabled)
- Google Cloud Project created and linked

### Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/nelsondca/Flood-Detection-System-FYP.git
    cd Flood-Detection-System-FYP
    ```

2. Set up the Python environment:
    ```bash
    python -m venv new_virtual_environment
    source new_virtual_environment/bin/activate  # or `venv\Scripts\activate` on Windows
    pip install -r requirements.txt
    ```

3. Authenticate Earth Engine:
    ```bash
    earthengine authenticate
    ```

4. Initialize Earth Engine:
    ```bash
    earthengine initialize
    ```

## How to Run

Run the Flask app:

```bash
python app.py

```

Then access the web interface at:
http://localhost:5000

Use the web interface to:

Select a city (e.g., Cork, Dublin, Galway, etc.)

View flood history and map visualizations

Analyze flood detection results

## For Development and Testing (Running the Jupyter Notebook)
Open GEEtest.ipynb.

Run the Jupyter Notebook to process satellite data

Choose a location (AOI — Area of Interest)

Visualize results and flood detection outputs

Launch the Leaflet.js frontend to explore the application

## Example
Running the frontend: Red areas show detected floodwater.

NDWI difference maps highlight changes before and after flood events.

## Output
The script will:

Display the processed area with the detection layers

Calculate the percentage of flood risk or flooded area

## Technologies Used
Google Earth Engine (GEE): Satellite imagery analysis.

Python: Core programming language.

geemap: Interactive mapping and GEE integration.

matplotlib: Data visualization.

rasterio: Raster file manipulation.

Jupyter Notebook: Development and prototyping.

Flask: Web application framework.

Leaflet.js: Web map visualization.

## Outputs
Visualizations

Pre-Flood and Post-Flood Images: Visualized using Sentinel-1 radar data.

NDWI Water Masks: Generated from Sentinel-2 optical data.

Flood Masks: Binary masks showing flooded areas.

Confusion Matrix: Heatmap showing validation results.

Metrics

Accuracy: Percentage of correctly identified flooded areas.

Precision: Percentage of detected floods that are correct.

Recall: Percentage of actual floods that were detected.

## Future Work
Improve Validation: Use additional datasets for better validation.

Enhance Web Interface: Add more interactive tools for users.

Automate Threshold Selection: Use machine learning to optimize thresholds for flood detection.

## Documentation/Research
Research papers, project documentation, and references used during the project can be found inside the /docs or cited in the main report.