from django.urls import path
from .views import (
    LoginView, LogoutView,LogoutRedirectView, UpdateLocationView,
    CyclewaysGeoJSONView, ParkingStandsGeoJSONView, MaintenanceStandsGeoJSONView,
    UserLocationView, LoginTemplateView, MapTemplateView, OfflineTemplateView,
    CheckAuthView, root_view
)

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/logout/', LogoutRedirectView.as_view(), name='api-logout'),
    path('api/location/', UpdateLocationView.as_view(), name='api-update-location'),
    path('api/cycleways/', CyclewaysGeoJSONView.as_view(), name='api-cycleways'),
    path('api/parking-stands/', ParkingStandsGeoJSONView.as_view(), name='api-parking-stands'),
    path('api/maintenance-stands/', MaintenanceStandsGeoJSONView.as_view(), name='api-maintenance-stands'),
    path('api/user-location/', UserLocationView.as_view(), name='api-user-location'),
    path('api/auth-check/', CheckAuthView.as_view(), name='auth-check'),
    
    # Template endpoints
    path('login/', LoginTemplateView.as_view(), name='login'),
    path('map/', MapTemplateView.as_view(), name='map'),
    path('offline/', OfflineTemplateView.as_view(), name='offline'),
    path('', root_view, name='root'),  # Root URL
]