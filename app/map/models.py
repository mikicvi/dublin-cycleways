from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.core.cache import cache

# Model definitions for each of the data sets that will be used in this application.


class BicycleMaintenanceStandSDCC(models.Model):
    """Model definition for Bicycle maintenance stands from South Dublin County Council.
    """
    featureID = models.IntegerField()
    featureID_internal = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()
    area = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    geometry = models.PointField()

    def __str__(self):
        return f"{self.area} - {self.location}"


class BicycleParkingStandSDCC(models.Model):
    """Model definition for Bicycle parking stands from South Dublin County Council.
    """
    featureID = models.IntegerField()
    featureID_internal = models.IntegerField(default=0)
    globalID = models.IntegerField()
    location = models.CharField(max_length=100)
    senior_stand = models.IntegerField()
    junior_stand = models.IntegerField()
    status = models.CharField(max_length=100)
    geometry = models.PointField()

    def __str__(self):
        return f"{self.location} - {self.status} - {self.senior_stand} - {self.junior_stand}"


class DublinCityParkingStand(models.Model):
    """
    Model for bicycle parking stands in Dublin City.
    """
    # Basic Fields
    osm_id = models.CharField(max_length=100, unique=True)  # From "id" field
    bicycle_parking = models.CharField(max_length=50, null=True, blank=True)
    covered = models.CharField(max_length=10, null=True, blank=True)
    capacity = models.CharField(max_length=5, null=True, blank=True)
    surveillance = models.CharField(max_length=10, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    fee = models.CharField(max_length=10, null=True, blank=True)

    # Geometry Field
    geometry = models.PointField()

    def __str__(self):
        return f"Parking Stand {self.osm_id} - {self.capacity or 'Unknown'}"
    
class BikeMaintenanceStandFCC(models.Model):
    """Model definition for Bicycle maintenance stands from Fingal County Council.
    """
    featureID = models.IntegerField()
    featureID_internal = models.IntegerField()
    location = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    public_stands = models.IntegerField(default=0, null=True, blank=True)
    private_stands = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.CharField(max_length=20)
    stand_type = models.CharField(max_length=100)
    geometry = models.PointField()

    def __str__(self):
        return f"{self.area} - {self.location} - {self.stand_type} - {self.public_stands} - {self.private_stands}"


class BikeMaintenanceStandDLR(models.Model):
    """Model definition for Bicycle maintenance stands from Dun Laoghaire Rathdown County Council.
    """
    featureID = models.IntegerField()
    featureID_internal = models.IntegerField()
    maintenance_point = models.CharField(max_length=3)
    covered = models.CharField(max_length=3)
    confirmed = models.CharField(max_length=3)
    geometry = models.PointField()

    def __str__(self):
        return f"{self.featureID} - {self.covered} - {self.confirmed}"


class CyclewaysSDCC(models.Model):
    """Model definition for Cycleways from South Dublin County Council.
    """
    featureID = models.IntegerField()
    name = models.CharField(max_length=255)
    colour = models.IntegerField()
    linetype = models.CharField(max_length=50, null=True)
    linewt = models.IntegerField()
    refname = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    geometry = models.LineStringField()
  
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('cycleways_geojson')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete('cycleways_geojson')  

    def __str__(self):
        return f"{self.featureID} - {self.name}"

    
class CyclewaysDublinMetro(models.Model):
    """Model definition for Cycleways for Dublin Metropolitan area.
    """
    # No feature id in data set, auto incrementing id will be used.
    featureID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    twoway = models.CharField(max_length=1)
    bollard_protected = models.CharField(max_length=1)
    shape_length = models.CharField(max_length=255)
    geometry = models.LineStringField()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('cycleways_geojson')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete('cycleways_geojson')
    
    def __str__(self):
        return f"{self.featureID} - {self.name} - {self.twoway} - {self.bollard_protected}"

class YellowCyclingInfrastructure(models.Model):
    """Model definition for Yellow Cycling Infrastructure - Non segregated - Dublin County.
    """
    name = models.CharField(max_length=255, null=True, blank=True)
    geometry = models.MultiLineStringField()
    
    def __str__(self):
        return f"{self.name or 'Unnamed'}"
    
class RedCyclingInfrastructure(models.Model):
    """Model definition for Red Cycling Infrastructure - No cycling infrastructure - Dublin County.
    """
    name = models.CharField(max_length=255, null=True, blank=True)
    geometry = models.MultiLineStringField()
    
    def __str__(self):
        return f"{self.name or 'Unnamed'}"

class CountyRoad(models.Model):
    """
    Model for all public roads in Dublin County.
    
    Note: Development model only used to calculate differences.
    """
    name = models.CharField(max_length=255, null=True, blank=True)
    geometry = models.MultiLineStringField()

    def __str__(self):
        return self.name or "Unnamed Road"

class CountyCycleway(models.Model):
    """
    Model for all cycleways in Dublin County.
    
    Note: Development model only used to calculate differences.
    """
    name = models.CharField(max_length=255, null=True, blank=True)
    geometry = models.MultiLineStringField()

    def __str__(self):
        return self.name or "Unnamed Cycleway"
    

# # User Profile model
User = get_user_model()


class Profile(models.Model):
    """
    Profile model extends the Django user model to include a location field.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the Django User model.
        location (PointField): A geographic point field to store the user's location, can be null or blank.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.PointField(null=True, blank=True)

    def __str__(self):
        return self.user.username
