from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from map.models import( 
BicycleMaintenanceStandSDCC, 
BicycleParkingStandSDCC, 
BikeMaintenanceStandFCC, 
BikeMaintenanceStandDLR, 
CyclewaysSDCC,
CyclewaysDublinMetro
)

def convert_to_float(value):
    try:
        return float(value)
    except ValueError:
        return None


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
    },
    {
        'model': BikeMaintenanceStandFCC,
        'geojson_path':  Path(__file__).resolve().parent / 'data' / 'Bike_Maintenance_Stands_2020_2021_2022_FCC.geojson',
        'mapping': {
                'featureID': 'OBJECTID',
                'featureID_internal': 'Id',
                'location': 'Location',
                'area': 'Area',
                'public_stands': 'Public_',
                'private_stands': 'Private',
                'date_added': 'Date_Added',
                'stand_type': 'Stand_Type',
                'geometry': 'POINT',
        }
    },
    {
        'model': BikeMaintenanceStandDLR,
        'geojson_path':  Path(__file__).resolve().parent / 'data' / 'dlr-bicycle-maintenance-stands.json',
        'mapping': {
                'featureID': 'OBJECTID',
                'featureID_internal': 'id',
                'maintenance_point': 'MaintenancePoint',
                'covered': 'covered',
                'confirmed': 'Confirmed',
                'geometry': 'POINT',
        }
    },
    {
        'model': CyclewaysSDCC,
        'geojson_path': Path(__file__).resolve().parent / 'data' / 'SDCC_Cycleways_-1477972845665274852.geojson',
        'mapping': {
            'featureID': 'OBJECTID',
            'name': 'Layer',
            'colour': 'Color',
            'linetype': 'Linetype',
            'linewt': 'LineWt',
            'refname': 'RefName',
            'description': 'Description',
            'geometry' : 'LineString',
        }
    }, 
    {
        'model': CyclewaysDublinMetro,
        'geojson_path': Path(__file__).resolve().parent / 'data' / 'segregated_cycle_infrastructure_dublinmetro.geojson',
        'mapping': {
            'name': 'Name',
            'twoway': 'twoway',
            'bollard_protected': 'bollardpro',
            'shape_length': 'Shape_Leng',
            'geometry': 'LineString',
        }
    }
]

def run(verbose=True):
    for dataset in datasets:
        print(f"Data loaded for {dataset['model'].__name__}")
        lm = LayerMapping(dataset['model'], dataset['geojson_path'], dataset['mapping'], transform=False)
        lm.save(strict=True, verbose=verbose)