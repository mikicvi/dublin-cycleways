from django.core.serializers import serialize
import json

from .models import (
    CyclewaysSDCC,
    CyclewaysDublinMetro,
    BicycleParkingStandSDCC,
    BicycleMaintenanceStandSDCC,
    BikeMaintenanceStandFCC,
    BikeMaintenanceStandDLR,
    DublinCityParkingStand,
    RedCyclingInfrastructure, 
    YellowCyclingInfrastructure
)


def serialize_cycleways_sdcc():
    """
    Serialize CyclewaysSDCC to GeoJSON.
    """
    data = serialize(
        'geojson',
        CyclewaysSDCC.objects.all(),
        geometry_field='geometry',
        fields=['featureID', 'name', 'colour', 'linetype', 'refname', 'description'],
    )
    return json.loads(data)


def serialize_cycleways_dublin_metro():
    """
    Serialize CyclewaysDublinMetro to GeoJSON.
    """
    data = serialize(
        'geojson',
        CyclewaysDublinMetro.objects.all(),
        geometry_field='geometry',
        fields=['featureID', 'name', 'twoway', 'bollard_protected', 'shape_length'],
    )
    return json.loads(data)


def serialize_bicycle_parking_stands_sdcc():
    """
    Serialize BicycleParkingStandSDCC to GeoJSON.
    """
    data = serialize(
        'geojson',
        BicycleParkingStandSDCC.objects.all(),
        geometry_field='geometry',
        fields=['featureID', 'featureID_internal', 'x', 'y', 'area', 'location'],
    )
    return json.loads(data)
import json

def serialize_dublin_city_parking_stands():
    """
    Serialize DublinCityParkingStand to GeoJSON.
    """
    data = serialize(
        'geojson',
        DublinCityParkingStand.objects.all(),
        geometry_field='geometry',
        fields=[
            'osm_id',
            'bicycle_parking',
            'covered',
            'capacity',
            'surveillance',
            'website',
            'fee',
        ],
    )
    return json.loads(data)

def serialize_bicycle_maintenance_stands_sdcc():
    """
    Serialize BicycleMaintenanceStandSDCC to GeoJSON.
    """
    data = serialize(
        'geojson',
        BicycleMaintenanceStandSDCC.objects.all(),
        geometry_field='geometry',
        fields=['featureID', 'featureID_internal', 'x', 'y', 'area', 'location'],
    )
    return json.loads(data)


def serialize_bike_maintenance_stands_fcc():
    """
    Serialize BikeMaintenanceStandFCC to GeoJSON.
    """
    data = serialize(
        'geojson',
        BikeMaintenanceStandFCC.objects.all(),
        geometry_field='geometry',
        fields=[
            'featureID',
            'featureID_internal',
            'location',
            'area',
            'public_stands',
            'private_stands',
            'date_added',
            'stand_type',
        ],
    )
    return json.loads(data)


def serialize_bike_maintenance_stands_dlr():
    """
    Serialize BikeMaintenanceStandDLR to GeoJSON.
    """
    data = serialize(
        'geojson',
        BikeMaintenanceStandDLR.objects.all(),
        geometry_field='geometry',
        fields=['featureID', 'featureID_internal', 'maintenance_point', 'covered', 'confirmed'],
    )
    return json.loads(data)


def serialize_red_cycling_infrastructure():
    """
    Serialize RedCyclingInfrastructure to GeoJSON.
    """
    data = serialize(
        'geojson',
        RedCyclingInfrastructure.objects.all(),
        geometry_field='geometry',
        fields=['name'],
    )
    return json.loads(data)


def serialize_yellow_cycling_infrastructure():
    """
    Serialize YellowCyclingInfrastructure to GeoJSON.
    """
    data = serialize(
        'geojson',
        YellowCyclingInfrastructure.objects.all(),
        geometry_field='geometry',
        fields=['name'],
    )
    return json.loads(data)