from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from map.models import CountyRoad, CountyCycleway
from pathlib import Path

class Command(BaseCommand):
    help = "Load normalized GeoJSON files into the database."

    def handle(self, *args, **options):
        base_path = Path(__file__).resolve().parent.parent.parent / 'data'

        datasets = [
            {
                'model': CountyRoad,
                'geojson_path': base_path / 'normalized-roads.geojson',
                'mapping': {'name': '@id', 'geometry': 'MultiLineString'},
            },
            {
                'model': CountyCycleway,
                'geojson_path': base_path / 'filtered-cycleways.geojson',
                'mapping': {'name': '@id', 'geometry': 'MultiLineString'},
            }
        ]

        for dataset in datasets:
            print(f"Loading {dataset['geojson_path']}...")
            lm = LayerMapping(dataset['model'], dataset['geojson_path'], dataset['mapping'], transform=False)
            lm.save(strict=True, verbose=True)
        print("Data loaded successfully.")