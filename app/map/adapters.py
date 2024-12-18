import urllib
import json

def fetch_dublin_bikes_geojson():
    """
    Fetch Dublin Bikes API and serialize to GeoJSON using urllib.
    """
    url = 'https://data.smartdublin.ie/dublinbikes-api/bikes/dublin_bikes/current/stations.geojson'
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                features = data['features']
                transformed_features = []

                for feature in features:
                    geometry = feature['geometry']
                    properties = feature['properties']
                    transformed_feature = {
                        'type': 'Feature',
                        'geometry': geometry,
                        'properties': {
                            'Name': properties['address'],
                            'Station Number': properties['station_id'],
                            'Bikes Available': properties['num_bikes_available'],
                            'Free Stations': properties['num_docks_available'],
                        }
                    }
                    transformed_features.append(transformed_feature)

                transformed_data = {
                    'type': 'FeatureCollection',
                    'features': transformed_features
                }

                return transformed_data
            else:
                raise Exception(f"Request failed with status code: {response.status}")
    except urllib.error.HTTPError as e:
        return {'error': f"HTTP Error: {e.code} - {e.reason}"}
    except urllib.error.URLError as e:
        return {'error': f"URL Error: {e.reason}"}

import urllib.request
import json

def fetch_general_bikes_geojson(url):
    """
    Fetch Bleeper Bikes API and serialize to GeoJSON using urllib.
    Handles cases where 'vehicle_type_id' is missing or not in the expected format.
    """
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                features = data.get('features', [])
                transformed_features = []

                for feature in features:
                    geometry = feature.get('geometry', {})
                    properties = feature.get('properties', {})

                    # Handle vehicle_type_id safely
                    vehicle_type_id = properties.get('vehicle_type_id', None)
                    if vehicle_type_id:
                        # Extract part after colon only if format matches 'something:E_BIKE'
                        vehicle_type_id = (
                            vehicle_type_id.split(':')[-1]
                            if ':' in vehicle_type_id
                            else None # Otherwise, set to None
                        )

                    # Transform feature
                    transformed_feature = {
                        'type': 'Feature',
                        'geometry': geometry,
                        'properties': {
                            'Bike ID': properties.get('bike_id', 'N/A'),
                            'Bike Type': vehicle_type_id,
                            'Is Reserved': str(properties.get('is_reserved', False)),
                            'Is Disabled': str(properties.get('is_disabled', False)),
                            'Fuel Percent': properties.get('current_fuel_percent'),
                            'Last Updated': properties.get('last_updated_dt', 'N/A'),
                        },
                    }
                    transformed_features.append(transformed_feature)

                # Final GeoJSON structure
                transformed_data = {
                    'type': 'FeatureCollection',
                    'features': transformed_features,
                }
                return transformed_data
            else:
                raise Exception(f"Request failed with status code: {response.status}")
    except urllib.error.HTTPError as e:
        return {'error': f"HTTP Error: {e.code} - {e.reason}"}
    except urllib.error.URLError as e:
        return {'error': f"URL Error: {e.reason}"}
    except Exception as e:
        return {'error': str(e)}

