import urllib
import json

def fetch__dublin_bikes_geojson():
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
