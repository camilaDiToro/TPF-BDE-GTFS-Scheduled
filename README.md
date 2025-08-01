# GTFS Scheduled Analysis: NYC Bus System

This repository contains the Python code used for analyzing GTFS (General Transit Feed Specification) scheduled data for the New York City bus system. The project is part of the final assignment for the course **73.38 - Spatial and Mobility Databases**.

## 📌 Project Description

The goal of this project is to explore, load, visualize, and analyze public transport data in NYC. The first phase focuses on scheduled GTFS data, with analyses including:

- Visualization of bus routes from different perspectives
- Aggregation of routes by common segments
- Identification of hot spots and overlapping routes
- Analysis of planned speeds in various districts

PostgreSQL and PostGIS are used to manage and query the spatial data, and the results are visualized using Python libraries such as `GeoPandas`, `Folium`, and `psycopg2`.

---

## 🛠️ Requirements

Install the required packages using:

```bash
pip install -r requirements.txt
```

> Make sure you have PostgreSQL and PostGIS properly installed and configured.

---

## ⚙️ Configuration

Before running the scripts, create a `config.yaml` file based on the provided template:

```yaml
# config_template.yaml
db_host: your_actual_host
db_name: your_actual_database
db_user: your_actual_username
db_password: your_actual_password
```

Rename it to `config.yaml` and complete it with your local database credentials.

---

## 🚀 Usage

The scripts in this repository connect to your local PostgreSQL/PostGIS database and perform different tasks, such as:

- Loading shapefiles for NYC boroughs
- Querying GTFS data from the database
- Visualizing bus routes and route segments
- Analyzing route overlap and planned bus speeds

Each script is modularized and can be run independently depending on the analysis you want to perform.

---

## 📂 Repository Organization

This repository is structured to mirror the sections of the written report for easier cross-reference and understanding. Each folder corresponds to a major chapter in the analysis, and the scripts are named to match the numbering used in the report.

The goal is for this repository to serve as **supporting material for the final project**, allowing readers to explore the code that underpins each part of the analysis.

```
3-loaders/                  # Scripts for loading GTFS data into PostgreSQL (Section 3 of the report)
5-routes_visualizations/    # Route visualizations: by shape, agency, type (Section 5)
6-segments/                 # Route segment construction and visualization (Section 6)
7-hot_spots/                # Hotspot detection, route overlaps, and spatial grids (Section 7)
8-speed/                    # Speed analysis and comparison between boroughs (Section 8)

db_utils/                   # Utility functions for DB connections
config_template.yaml        # Configuration template for DB credentials
```

Each script is prefixed with a number (e.g., `6-1-`, `7-3-`) that matches the subsection in the report. For example:

- `6-1-generate_brooklyn_segments.py` corresponds to Section **6.1**.
- `7-3-hot_spot_routes.py` corresponds to Section **7.3**.
- `8-2-velocity_comparation.py` corresponds to Section **8.2.2**.

The `/outputs/` folders in each section store visualizations (maps, layers) generated by those scripts.

> 📖 **Reading the report alongside this repository is recommended** for a full understanding of the analyses and methodology.

>⚠️ **Note**: The `outputs/` folders used to store generated visualizations (maps, layers, etc.) are ignored by Git and **do not appear after cloning the repository**. If they are missing, **please create them manually** inside each numbered folder before running the scripts.

---
