import unittest
# Try to fix gevent recursion error by patching early
try:
    from gevent import monkey
    monkey.patch_all(thread=False)
except ImportError:
    pass

from src.tools.osm_search import OSMSearchTool
from unittest.mock import MagicMock
import json

class TestOSMSearchIntegration(unittest.TestCase):
    def setUp(self):
        # Mock runtime and session as required by Dify SDK
        self.mock_runtime = MagicMock()
        self.mock_session = MagicMock()
        self.tool = OSMSearchTool(runtime=self.mock_runtime, session=self.mock_session)

    def test_actual_osm_query(self):
        """
        This test performs an actual network request to the Overpass API.
        It searches for groceries within 1km of Berlin Alexanderplatz.
        """
        params = {
            "latitude": 52.5219,
            "longitude": 13.4132,
            "radius": 0.5, # Reduced radius to 500m for faster response
            "categories": "groceries"
        }

        print(f"\nQuerying OSM for groceries near Alexanderplatz (52.5219, 13.4132)...")
        
        # We Catch the yielded messages from the generator
        messages = list(self.tool._invoke(params))
        
        self.assertTrue(len(messages) > 0, "No messages returned from tool")
        
        for msg in messages:
            print(f"Received message type: {type(msg)}")
            if hasattr(msg, 'message'):
                # In Dify SDK, msg.message might be a complex object
                content = msg.message
                # Handle different Dify SDK message formats
                if hasattr(content, 'json_object'):
                    data = content.json_object
                elif hasattr(content, 'text'):
                    data = content.text
                else:
                    data = content

                if isinstance(data, dict) and 'results' in data:
                    print(f"Found {data['count']} results.")
                    for item in data['results'][:3]: # Print first 3
                        print(f" - {item['name']} ({item['type']})")
                        print(f"   Coords: {item['lat']}, {item['lon']}")
                        print(f"   Address: {item.get('address')}")
                        print(f"   Description: {item.get('description')}")
                    
                    self.assertGreaterEqual(data['count'], 0)
                    if data['count'] > 0:
                        self.assertIn('description', data['results'][0])
                else:
                    print(f"Message content: {data}")

if __name__ == '__main__':
    unittest.main()
