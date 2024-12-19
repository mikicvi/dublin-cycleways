from django.urls import path
from .views import (
    BleeperBikesGeoJSONView, LoginView, LogoutView,LogoutRedirectView, MobyBikesGeoJSONView, RedCyclingInfrastructureGeoJSONView, RegisterTemplateView, RegisterView, UpdateLocationView,
    CyclewaysGeoJSONView, ParkingStandsGeoJSONView, MaintenanceStandsGeoJSONView,
    UserLocationView, LoginTemplateView, MapTemplateView, OfflineTemplateView,
    CheckAuthView, YellowCyclingInfrastructureGeoJSONView, root_view, DublinBikesGeoJSONView
)

urlpatterns = [
    # API endpoints
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/logout/', LogoutRedirectView.as_view(), name='api-logout'),
    path('api/location/', UpdateLocationView.as_view(), name='api-update-location'),
    path('api/cycleways/', CyclewaysGeoJSONView.as_view(), name='api-cycleways'),
    path('api/parking-stands/', ParkingStandsGeoJSONView.as_view(), name='api-parking-stands'),
    path('api/maintenance-stands/', MaintenanceStandsGeoJSONView.as_view(), name='api-maintenance-stands'),
    path('api/user-location/', UserLocationView.as_view(), name='api-user-location'),
    path('api/auth-check/', CheckAuthView.as_view(), name='auth-check'),
    path('api/dublin-bikes/',DublinBikesGeoJSONView.as_view(), name='dublin-bikes'),
    path('api/bleeper-bikes/',BleeperBikesGeoJSONView.as_view(), name='bleeper-bikes'),
    path('api/moby-bikes/',MobyBikesGeoJSONView.as_view(), name='moby-bikes'),
    path('api/red-cycling-infrastructure/', RedCyclingInfrastructureGeoJSONView.as_view(), name='red-cycling-geojson'),
    path('api/yellow-cycling-infrastructure/', YellowCyclingInfrastructureGeoJSONView.as_view(), name='yellow-cycling-geojson'),

    
    # Template endpoints
    path('login/', LoginTemplateView.as_view(), name='login'),
    path('register/', RegisterTemplateView.as_view(), name='register'),
    path('map/', MapTemplateView.as_view(), name='map'),
    path('offline/', OfflineTemplateView.as_view(), name='offline'),
    path('', root_view, name='root'),  # Root URL
]