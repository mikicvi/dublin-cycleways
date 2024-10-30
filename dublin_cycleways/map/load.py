from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from map.models import( BicycleMaintenanceStandSDCC, BicycleParkingStandSDCC)


datasets = [
    {
        'model': BicycleMaintenanceStandSDCC,
        'geojson_path':  Path(__file__).resolve().parent / 'data' / 'Bicycle_Maintenance_Stands_SDCC.geojson',
        'mapping': {
                'featureID': 'OBJECTID',
                'featureID_internal': 'OBJECTID_1',
                'x': 'X',
                'y': 'Y',
                'area': 'Area',
                'location': 'Location',
                'geometry': 'POINT',
        }
    },
    {
        'model': BicycleParkingStandSDCC,
        'geojson_path':  Path(__file__).resolve().parent / 'data' / 'Bicycle_Parking_Stands_SDCC.geojson',
        'mapping': {
                'featureID': 'FID',
                'featureID_internal': 'FID_1',
                'globalID': 'gid',
                'location': 'location',
                'senior_stand': 'senior_sta',
                'junior_stand': 'junior_sta',
                'status': 'status',
                'geometry': 'POINT',
        }
    }
]

def run(verbose=True):
    for dataset in datasets:
        print(f"Data loaded for {dataset['model'].__name__}")
        lm = LayerMapping(dataset['model'], dataset['geojson_path'], dataset['mapping'], transform=False)
        lm.save(strict=True, verbose=verbose)