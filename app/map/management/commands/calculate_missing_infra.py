import os
import logging
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import MultiLineString, GEOSGeometry
from django.contrib.gis.db.models.functions import Difference
from django.core.serializers import serialize
from map.models import (
    CountyRoad,
    CountyCycleway,
    CyclewaysSDCC,
    CyclewaysDublinMetro,
    RedCyclingInfrastructure,
    YellowCyclingInfrastructure,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Calculate and store roads with no cycling infrastructure (Red) and non-segregated cycling infrastructure (Yellow), and dump to GeoJSON."

    def handle(self, *args, **options):
        self.stdout.write("Calculating missing and non-segregated cycling infrastructure...")
        logger.info("Starting calculation of missing and non-segregated cycling infrastructure...")

        # Clear previous results
        RedCyclingInfrastructure.objects.all().delete()
        YellowCyclingInfrastructure.objects.all().delete()

        # Load geometries for both segregated cycleway models
        sdcc_geometries = CyclewaysSDCC.objects.values_list('geometry', flat=True)
        dublin_metro_geometries = CyclewaysDublinMetro.objects.values_list('geometry', flat=True)
        
        # Combine all segregated geometries
        segregated_geometries = list(sdcc_geometries) + list(dublin_metro_geometries)

        # Load all non-segregated cycleway geometries
        cycleway_geometries = CountyCycleway.objects.values_list('geometry', flat=True)

        # Process each public road
        total_roads = CountyRoad.objects.count()
        for index, road in enumerate(CountyRoad.objects.iterator(chunk_size=500)):
            road_geometry = road.geometry

            # Step 1: Subtract all segregated infrastructure
            for segregated in segregated_geometries:
                road_geometry = road_geometry.difference(segregated)

            # Step 2: Subtract non-segregated cycleways (remaining is Red)
            nonsegmented_geometry = road_geometry  # Save intermediate result for Yellow
            for cycleway in cycleway_geometries:
                road_geometry = road_geometry.difference(cycleway)

            # Save the road segments with no cycling infrastructure (Red)
            if not road_geometry.empty:
                if road_geometry.geom_type == 'LineString':  # Wrap LineString as MultiLineString
                    road_geometry = MultiLineString(road_geometry)
                RedCyclingInfrastructure.objects.create(
                    name=road.name,
                    geometry=road_geometry
                )

            # Save road segments with non-segregated cycling infrastructure (Yellow)
            if not nonsegmented_geometry.empty:
                if nonsegmented_geometry.geom_type == 'LineString':  # Wrap LineString as MultiLineString
                    nonsegmented_geometry = MultiLineString(nonsegmented_geometry)
                YellowCyclingInfrastructure.objects.create(
                    name=road.name,
                    geometry=nonsegmented_geometry
                )

            # Log progress
            if (index + 1) % 100 == 0:
                logger.info(f"Processed {index + 1}/{total_roads} roads")

        self.stdout.write(self.style.SUCCESS("Successfully calculated Red and Yellow infrastructure."))
        logger.info("Successfully calculated Red and Yellow infrastructure.")

        # Dump results to GeoJSON files
        output_dir = os.path.join(os.getcwd(), 'map', 'exports')
        os.makedirs(output_dir, exist_ok=True)

        # Dump Red infrastructure
        red_output_file = os.path.join(output_dir, 'red_infrastructure.geojson')
        with open(red_output_file, 'w') as f:
            red_data = serialize('geojson', RedCyclingInfrastructure.objects.all(), geometry_field='geometry', fields=('name',))
            f.write(red_data)
        self.stdout.write(self.style.SUCCESS(f"Red infrastructure dumped to {red_output_file}"))
        logger.info(f"Red infrastructure dumped to {red_output_file}")

        # Dump Yellow infrastructure
        yellow_output_file = os.path.join(output_dir, 'yellow_infrastructure.geojson')
        with open(yellow_output_file, 'w') as f:
            yellow_data = serialize('geojson', YellowCyclingInfrastructure.objects.all(), geometry_field='geometry', fields=('name',))
            f.write(yellow_data)
        self.stdout.write(self.style.SUCCESS(f"Yellow infrastructure dumped to {yellow_output_file}"))
        logger.info(f"Yellow infrastructure dumped to {yellow_output_file}")