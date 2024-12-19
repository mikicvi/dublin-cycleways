from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.gis.geos import Point
from .models import (
    Profile
)
from .serializers import (
    serialize_cycleways_sdcc,
    serialize_cycleways_dublin_metro,
    serialize_bicycle_parking_stands_sdcc,
    serialize_bicycle_maintenance_stands_sdcc,
    serialize_bike_maintenance_stands_fcc,
    serialize_bike_maintenance_stands_dlr,
    serialize_dublin_city_parking_stands,
    serialize_red_cycling_infrastructure,
    serialize_yellow_cycling_infrastructure
)
from .adapters import (
    fetch_general_bikes_geojson,
    fetch_dublin_bikes_geojson,
)
from django.shortcuts import render
from django.views import View
from drf_spectacular.utils import extend_schema

User = get_user_model()


# Login API
import logging
logger = logging.getLogger(__name__)

class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'password']
            }
        },
        responses={
            200: {'description': 'Login successful'},
            401: {'description': 'Invalid credentials'}
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({'message': 'Login successful'}, status=200)
        return Response({'error': 'Invalid credentials'}, status=401)
# Logout API
@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: {'description': 'Logout successful'}
        }
    )
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=200)
class LogoutRedirectView(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')

# Register API
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'email', 'password']
            }
        },
        responses={
            201: {'description': 'Registration successful'},
            400: {'description': 'Missing fields or user already exists'}
        }
    )
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if username and email and password:
            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=400)
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=400)
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return Response({'message': 'Registration successful'}, status=201)
        return Response({'error': 'Missing fields'}, status=400)


# Update Location API
class UpdateLocationView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'latitude': {'type': 'number'},
                    'longitude': {'type': 'number'}
                },
                'required': ['latitude', 'longitude']
            }
        },
        responses={
            200: {'description': 'Location updated successfully'},
            400: {'description': 'Invalid or missing coordinates'}
        }
    )
    def post(self, request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        if latitude and longitude:
            try:
                location = Point(float(longitude), float(latitude))
                profile, created = Profile.objects.get_or_create(user=request.user)
                profile.location = location
                profile.save()
                return Response({'status': 'success'}, status=200)
            except ValueError:
                return Response({'error': 'Invalid coordinates'}, status=400)
        return Response({'error': 'Missing coordinates'}, status=400)
    
# Map View API
class UserLocationView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'user': {'type': 'string'},
                    'location': {
                        'type': 'object',
                        'properties': {
                            'latitude': {'type': 'number'},
                            'longitude': {'type': 'number'}
                        }
                    }
                }
            },
            404: {'description': 'Location not set'}
        }
    )
    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        location = profile.location
        if location:
            return Response({
                'user': request.user.username,
                'location': {
                    'latitude': location.y,
                    'longitude': location.x
                }
            })
        return Response({'error': 'Location not set'}, status=404)

# Cycleways GeoJSON API
class CyclewaysGeoJSONView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'type': {'type': 'string'},
                    'features': {'type': 'array'}
                }
            }
        }
    )
    def get(self, request):
        # Serialize data
        sdcc_features = serialize_cycleways_sdcc()['features']
        dublin_metro_features = serialize_cycleways_dublin_metro()['features']

        # Combine features into a single FeatureCollection
        combined_geojson = {
            'type': 'FeatureCollection',
            'features': sdcc_features + dublin_metro_features,
        }

        return Response(combined_geojson)
    

# Red Cycling Infrastructure GeoJSON API
class RedCyclingInfrastructureGeoJSONView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'type': {'type': 'string'},
                    'features': {'type': 'array'}
                }
            }
        }
    )
    def get(self, request):
        red_geojson = serialize_red_cycling_infrastructure()
        return Response(red_geojson)


# Yellow Cycling Infrastructure GeoJSON API
class YellowCyclingInfrastructureGeoJSONView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'type': {'type': 'string'},
                    'features': {'type': 'array'}
                }
            }
        }
    )
    def get(self, request):
        yellow_geojson = serialize_yellow_cycling_infrastructure()
        return Response(yellow_geojson)

# Parking Stands GeoJSON API
class ParkingStandsGeoJSONView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'type': {'type': 'string'},
                    'features': {'type': 'array'}
                }
            }
        }
    )
    def get(self, request):
        sdcc_parking_features = serialize_bicycle_parking_stands_sdcc()['features']
        dcc_parking_features = serialize_dublin_city_parking_stands()['features']
        
        combined_geojson = {
            'type': 'FeatureCollection',
            'features': sdcc_parking_features + dcc_parking_features,
        }
        return Response(combined_geojson)

# Maintenance Stands GeoJSON API
class MaintenanceStandsGeoJSONView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'type': {'type': 'string'},
                    'features': {'type': 'array'}
                }
            }
        }
    )
    def get(self, request):
        dlr_features = serialize_bike_maintenance_stands_dlr()['features']
        fcc_features = serialize_bike_maintenance_stands_fcc()['features']
        sdcc_features = serialize_bicycle_maintenance_stands_sdcc()['features']

        combined_geojson = {
            'type': 'FeatureCollection',
            'features': dlr_features + fcc_features + sdcc_features,
        }

        return Response(combined_geojson)
    
# Dublin Bikes Live GeoJSON API
class DublinBikesGeoJSONView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'type': {'type': 'string'},
                    'features': {'type': 'array'}
                }
            },
            500: {'description': 'Error fetching data'}
        }
    )
    def get(self, request):
            data = fetch_dublin_bikes_geojson()
            if 'Error' in data:
                return Response(data, status=500)
            return Response(data)

# Bleeper Bikes Live GeoJSON API
class BleeperBikesGeoJSONView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'type': {'type': 'string'},
                    'features': {'type': 'array'}
                }
            },
            500: {'description': 'Error fetching data'}
        }
    )
    def get(self, request):
        data = fetch_general_bikes_geojson('https://data.smartdublin.ie/bleeperbike-api/bikes/bleeper_bikes/current/bikes.geojson')
        if 'Error' in data:
            return Response(data, status=500)
        return Response(data)

# Moby Bikes Live GeoJSON API
class MobyBikesGeoJSONView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'type': {'type': 'string'},
                    'features': {'type': 'array'}
                }
            },
            500: {'description': 'Error fetching data'}
        }
    )
    def get(self, request):
        data = fetch_general_bikes_geojson('https://data.smartdublin.ie/mobybikes-api/bikes/mobymoby_dublin/current/bikes.geojson')
        if 'Error' in data:
            return Response(data, status=500)
        return Response(data)
# Check Auth API
class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'authenticated': {'type': 'boolean'},
                    'username': {'type': 'string'}
                }
            }
        }
    )
    def get(self, request):
        return Response({'authenticated': True, 'username': request.user.username})



# Simple Django views to render the templated
class LoginTemplateView(View):
    def get(self, request):
        return render(request, 'login.html')

class RegisterTemplateView(View):
    def get(self, request):
        return render(request, 'register.html')

class MapTemplateView(View):
    def get(self, request):
        context = {
        'MAPBOX_API_KEY': settings.MAPBOX_API_KEY,
            }
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'map.html', context)

class OfflineTemplateView(View):
    def get(self, request):
        return render(request, 'offline.html')

def root_view(request):
    if request.user.is_authenticated:
        return redirect('map')  # Redirect to the map
    return redirect('login')  # Redirect to the login page