from django.contrib import admin
from map.models import( 
BicycleMaintenanceStandSDCC, 
BicycleParkingStandSDCC, 
BikeMaintenanceStandFCC, 
BikeMaintenanceStandDLR, 
CyclewaysSDCC,
CyclewaysDublinMetro
)


# Register your models here.
admin.site.register(BicycleMaintenanceStandSDCC)
admin.site.register(BicycleParkingStandSDCC)
admin.site.register(BikeMaintenanceStandFCC)
admin.site.register(BikeMaintenanceStandDLR)
admin.site.register(CyclewaysSDCC)
admin.site.register(CyclewaysDublinMetro)

