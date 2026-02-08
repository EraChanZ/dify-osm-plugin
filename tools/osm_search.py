from collections.abc import Generator
from typing import Any
import requests
import logging

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.config.logger_format import plugin_logger_handler

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(plugin_logger_handler)

class OSMSearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        try:
            lat = float(tool_parameters.get("latitude"))
            lon = float(tool_parameters.get("longitude"))
            radius_km = float(tool_parameters.get("radius", 1.0))
            categories = tool_parameters.get("categories", "")
            
            logger.info(f"OSM Search: lat={lat}, lon={lon}, radius={radius_km}km, categories={categories}")
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid input parameters: {str(e)}")
            yield self.create_text_message(f"Error: Invalid input parameters - {str(e)}")
            return

        # Map categories to Overpass tags
        category_map = {
            "groceries": '["shop"~"supermarket|convenience|grocery|bakery"]',
            "restaurants": '["amenity"~"restaurant|cafe|fast_food|pub"]',
            "transportation": '["amenity"~"bus_station|train_station|bicycle_parking|fuel"]',
            "pharmacies": '["amenity"~"pharmacy"]',
            "banks": '["amenity"~"bank|atm"]',
            "parks": '["leisure"~"park|garden"]',
            "hospitals": '["amenity"~"hospital|clinic|doctors"]'
        }
        
        tag_filter = category_map.get(categories.lower(), "")
        radius_meters = radius_km * 1000
        
        # Build Overpass QL query
        # We search for nodes, ways, and relations within the radius
        query = f"""
        [out:json][timeout:25];
        (
          node{tag_filter}(around:{radius_meters},{lat},{lon});
          way{tag_filter}(around:{radius_meters},{lat},{lon});
          relation{tag_filter}(around:{radius_meters},{lat},{lon});
        );
        out center;
        """
        
        try:
            response = requests.post("https://overpass-api.de/api/interpreter", data={"data": query}, timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            logger.error(f"Error querying Overpass API: {str(e)}")
            yield self.create_text_message(f"Error: Failed to fetch data from OpenStreetMap - {str(e)}")
            return

        elements = data.get("elements", [])
        results = []
        
        for el in elements:
            tags = el.get("tags", {})
            name = tags.get("name", "Unnamed")
            
            # Get coordinates (center for ways/relations)
            el_lat = el.get("lat") or el.get("center", {}).get("lat")
            el_lon = el.get("lon") or el.get("center", {}).get("lon")
            
            # Format address
            addr_parts = [
                tags.get("addr:housenumber"),
                tags.get("addr:street"),
                tags.get("addr:city")
            ]
            address = ", ".join([p for p in addr_parts if p]) or "Address unknown"
            
            # Create description
            desc_parts = []
            if tags.get("shop"): desc_parts.append(f"Shop: {tags['shop']}")
            if tags.get("amenity"): desc_parts.append(f"Amenity: {tags['amenity']}")
            if tags.get("leisure"): desc_parts.append(f"Leisure: {tags['leisure']}")
            description = " | ".join(desc_parts) or "No description available"
            
            results.append({
                "name": name,
                "type": el.get("type"),
                "lat": el_lat,
                "lon": el_lon,
                "address": address,
                "description": description,
                "tags": tags
            })

        yield self.create_json_message({
            "count": len(results),
            "results": results
        })

        if not results:
            yield self.create_text_message("No locations found matching your criteria in this area.")
        else:
            yield self.create_text_message(f"Found {len(results)} locations nearby.")
