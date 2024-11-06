from django.shortcuts import render, redirect
from django.core.cache import cache
from django.core.serializers import serialize
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, get_user_model, logout, authenticate
from django.contrib.gis.geos import Point, LineString
from django.http import JsonResponse
from .models import CyclewaysSDCC, CyclewaysDublinMetro, Profile
import json

User = get_user_model()

# Login & logout views
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('map')  # Redirect to the main map view
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def set_user_location(user_id, latitude, longitude):
    user = User.objects.get(id=user_id)
    location = Point(longitude, latitude) # Point takes longitude and latitude

    ## Create or update the user's profile
    profile, created = Profile.objects.get_or_create(user=user)
    profile.location = location
    profile.save()

    return profile

def update_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        if latitude and longitude:
            try:
                latitude = float(latitude)
                longitude = float(longitude)
                location = Point(longitude, latitude)

                profile, created = Profile.objects.get_or_create(user=request.user)
                if profile.location != location:
                    profile.location = location
                    profile.save()
                return JsonResponse({'status': 'success'})
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Invalid coordinates'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Missing coordinates'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    


def map_view(request):
    if request.user.is_authenticated:
        # Ensure the user has a profile
        user_profile, created = Profile.objects.get_or_create(user=request.user)
        location = user_profile.location
        return render(request, 'map.html', {'user': request.user, 'location': location})
    else:
        return redirect('login')
    

def cycleways_geojson(request):
    if request.user.is_authenticated:
        # cache for performance reasons
        cache_key = 'cycleways_geojson'
        cached_data = cache.get(cache_key)
        sdcc_cycleways = CyclewaysSDCC.objects.all()
        
        if cached_data:
            return JsonResponse(cached_data)
        
        # No cached data, so query the database
        dublin_metro_cycleways = CyclewaysDublinMetro.objects.all()

        # Serialize the querysets to GeoJSON
        sdcc_geojson = serialize('geojson', sdcc_cycleways, geometry_field='geometry', fields=(
            'featureID', 'name', 'colour', 'linetype', 'refname', 'description'))
        dublin_metro_geojson = serialize('geojson', dublin_metro_cycleways, geometry_field='geometry', fields=(
            'featureID', 'name', 'twoway', 'bollard_protected', 'shape_length'))

        # Combine the features
        sdcc_features = json.loads(sdcc_geojson)['features']
        dublin_metro_features = json.loads(dublin_metro_geojson)['features']
        combined_features = sdcc_features + dublin_metro_features

        combined_geojson = {
            'type': 'FeatureCollection',
            'features': combined_features
        }

        cache.set(cache_key, combined_geojson, None)  # Cache indefinitely
        return JsonResponse(combined_geojson)
    else:
        return redirect('login')
    