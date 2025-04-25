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
This project was developed as a Final Year Project, with a focus on flood detection with satellite data and geospatial analysis. Google Earth Engine (GEE) is used in the system for processing Sentinel-1 radar and Sentinel-2 optical data for detecting and visualizing flooded areas.

The system has Cork, Ireland, as its case study location, which experienced record flooding in October 2023. The project combines advanced geospatial processing with an intuitive web interface for visualization.

The system focuses on Cork, Ireland as a case study area, which experienced significant flooding in October 2023, but it is adapted and can analyze any other area in the map.

## Installation

**Note**: To use this project, you must have your own Google Earth Engine account.  
Sign up for free at [Google Earth Engine Signup](https://signup.earthengine.google.com/).

### Prerequisites
- Python 3.8+
- Google Earth Engine account (with API enabled)
- Google Cloud Poject Created

### Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/nelsondca/Flood-Detection-System-FYP.git
    cd Flood-Detection-System-FYP
    ```

2. Set up Python environment:
    ```bash
    python -m venv new_virtual_environment
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Authenticate Earth Engine:
    ```bash
    earthengine authenticate
    ```

4. Initiate Earth Engine:
    ```bash
    earthengine initialize
    ```

## How to Run

```bash
python app.py
```

Then access the web interface at: 
in my case is http://localhost:5000

Use the web interface to:

Select a city (e.g., Cork, Dublin, Galway, etc.).
View flood history and map visualizations.
Analyze flood detection results.

## For development and testing Running the Jupyter Notebook:

Open GEEtest.ipynb 

- Run the jupyter Notebooks to process satellite data.
- Choose a location ( AOI )
- Visualize results and flood detection outputs
- Launch the Leaflet.js frontend to explore the application

## Example

- Runing front end Red areas show detected floodwater.
- NDWI difference maps highlight changes before and after flood events.

## Output

- The script will:
    Display the processed area with the detection layers
    Percentage of flood risk or area flooded

## Technologies Used

- Google Earth Engine (GEE): Satellite imagery analysis.
- Python: Core programming language.
- geemap: Interactive mapping and GEE integration.
- matplotlib: Data visualization.
- rasterio: Raster file manipulation.
- Jupyter Notebook: Development and prototyping.
- Flask: Web application framework.
- Leaflet.js: Web map visualization.

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
Expand AOI: Include additional regions for analysis.
Improve Validation: Use additional datasets (e.g., JRC water data) for validation.
Enhance Web Interface: Add more interactive tools for users.
Automate Threshold Selection: Use machine learning to optimize thresholds for flood detection.
