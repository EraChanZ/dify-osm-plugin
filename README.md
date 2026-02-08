# OpenStreetMap Plugin for Dify

This plugin integrates OpenStreetMap (OSM) into Dify, enabling AI agents to search for local amenities and calculate walking distances. It provides agents with real-world spatial awareness without requiring expensive proprietary mapping APIs.

## Why this Plugin?

### 🌍 Real-World Context for AI
Most LLMs have a "cutoff date" and lack real-time knowledge of local businesses, parks, or transit. This plugin bridges that gap, allowing your Dify agents to answer questions like:
- "What are the closest grocery stores to this apartment?"
- "Is there a park within walking distance of my current location?"
- "Find me a pharmacy near Alexanderplatz."

### ⚡ Efficient & Cost-Effective
- **No API Keys Required**: Uses the public Overpass API (OpenStreetMap), eliminating the need for Google Maps or Mapbox API keys and their associated costs.
- **Privacy-First**: Queries are made directly to OpenStreetMap's community-driven infrastructure.
- **Lightweight**: Optimized Overpass QL queries ensure fast responses even for complex category searches.

### 🚶 Specialized Tools
- **OSM Search**: Deep search for specific amenities (Groceries, Restaurants, Healthcare, etc.) with radius control.
- **Walking Distance**: A utility to calculate the estimated walking time between two coordinates using the Haversine formula, helping agents provide practical logistics advice.

## Features

- **Amenity Search**: Find specific types of locations including:
  - **Groceries**: Supermarkets, convenience stores, bakeries, etc.
  - **Restaurants**: Cafes, pubs, and fast food.
  - **Parks**: Public parks and leisure areas.
  - **Healthcare**: Hospitals, clinics, pharmacies, and doctors.
  - **Transportation**: Bus stations, fuel, and train stations.
  - **Banks**: Banks and ATMs.
- **Radius Control**: Search within a customizable distance (in kilometers).
- **Detailed Information**: Returns names, types, coordinates, and addresses (where available).

## Installation

1. Package the plugin:
   ```bash
   dify plugin package .
   ```
2. Upload the generated `.difypkg` file to your Dify instance.

## Usage

### 1. OSM Search Tool (`osm_search`)
- `latitude` (Number): The latitude of the center point.
- `longitude` (Number): The longitude of the center point.
- `radius` (Number): Search radius in kilometers (default: 1.0).
- `categories` (Select): The category of amenities (e.g., `groceries`, `restaurants`, `parks`).

### 2. Walking Distance Tool (`walking_distance`)
- `from_lat`, `from_lon`: Starting coordinates.
- `to_lat`, `to_lon`: Destination coordinates.
- `walking_speed`: Speed in km/h (default: 5.0).

## Development & Testing

To run tests locally, ensure you have `uv` installed and set the `PYTHONPATH`:

```powershell
# PowerShell
$env:PYTHONPATH = "."; uv run python tests/test_osm_integration.py

# Bash
PYTHONPATH=. uv run python tests/test_osm_integration.py
```

## License

MIT
