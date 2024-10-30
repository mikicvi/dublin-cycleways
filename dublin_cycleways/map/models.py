from django.db import models
from django.contrib.gis.db import models as gis_models


class BicycleMaintenanceStandSDCC(models.Model):
    """Model definition for Bicycle maintenance stands from South Dublin County Council.
    """
    featureID = models.IntegerField()
    featureID_internal = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()
    area = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    geometry = gis_models.PointField()

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
    geometry = gis_models.PointField()

    def __str__(self):
        return f"{self.location} - {self.status} - {self.senior_stand} - {self.junior_stand}"



