import unittest
from unittest.mock import patch, MagicMock
from src.tools.osm_search import OSMSearchTool

class TestOSMSearchTool(unittest.TestCase):
    def setUp(self):
        # Mock runtime and session
        self.mock_runtime = MagicMock()
        self.mock_session = MagicMock()
        self.tool = OSMSearchTool(runtime=self.mock_runtime, session=self.mock_session)

    @patch('requests.post')
    def test_osm_search_invoke(self, mock_post):
        # Mock OSM response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "elements": [
                {
                    "type": "node",
                    "lat": 52.5200,
                    "lon": 13.4050,
                    "tags": {
                        "name": "Test Supermarket",
                        "shop": "supermarket",
                        "addr:street": "Main St",
                        "addr:housenumber": "1"
                    }
                }
            ]
        }
        mock_post.return_value = mock_response

        params = {
            "latitude": 52.5200,
            "longitude": 13.4050,
            "radius": 1.0,
            "categories": "groceries"
        }

        # We need to mock the create_json_message method as it's part of the Tool base class
        with patch.object(self.tool, 'create_json_message') as mock_json_msg:
            list(self.tool._invoke(params))
            
            mock_json_msg.assert_called_once()
            result_data = mock_json_msg.call_args[0][0]
            self.assertEqual(result_data["count"], 1)
            self.assertEqual(result_data["results"][0]["name"], "Test Supermarket")
            self.assertEqual(result_data["results"][0]["address"], "1, Main St")
            self.assertIn("description", result_data["results"][0])

if __name__ == '__main__':
    unittest.main()
