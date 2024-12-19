from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from django.contrib.auth.models import User
from map.models import BicycleParkingStandSDCC, Profile
from django.contrib.gis.geos import Point


class MapsAPITestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile(user=self.user)
        self.profile.save()
        self.parking_stand = BicycleParkingStandSDCC(
            featureID=1,
            featureID_internal=1,
            globalID=1,
            location='Test Location',
            senior_stand=10,
            junior_stand=5,
            status='Active',
            geometry=Point(1, 1)
        )
        self.parking_stand.save()
        self.login_url = reverse('api-login')
        self.logout_url = reverse('api-logout')
        self.register_url = reverse('api-register')
        self.update_location_url = reverse('api-update-location')
        self.parking_stands_url = reverse('api-parking-stands')
        self.cycleways_url = reverse('api-cycleways')
        self.maintenance_stands_url = reverse('api-maintenance-stands')
        self.user_location_url = reverse('api-user-location')
        self.auth_check_url = reverse('auth-check')
        self.dublin_bikes_url = reverse('dublin-bikes')
        self.bleeper_bikes_url = reverse('bleeper-bikes')
        self.moby_bikes_url = reverse('moby-bikes')
        self.red_cycling_geojson_url = reverse('red-cycling-geojson')
        self.yellow_cycling_geojson_url = reverse('yellow-cycling-geojson')
        


    @patch('map.views.authenticate')
    @patch('map.views.login')
    def test_login_success(self, mock_login, mock_authenticate):
        mock_authenticate.return_value = self.user
        data = {'username': 'testuser', 'password': 'testpassword'}

        # Send the POST request
        response = self.client.post(self.login_url, data, format='json')
        
        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Login successful')

    # Mocked tests section

    @patch('map.views.Profile.objects.get_or_create')
    def test_update_location_view(self, mock_get_or_create):
        mock_get_or_create.return_value = (self.profile, True)
        self.client.force_authenticate(user=self.user)

        data = {'latitude': 53.3498, 'longitude': -6.2603}
        response = self.client.post(self.update_location_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        mock_get_or_create.assert_called_once_with(user=self.user)

    def test_login_failure(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        self.assertIn('error', response.data)  
        self.assertEqual(response.data['error'], 'Invalid credentials')

    @patch('map.views.User.objects.create_user')
    def test_register_view(self, mock_create_user):
        mock_create_user.return_value = self.user
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpassword'}
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Registration successful')
        mock_create_user.assert_called_once_with(username='newuser', email='newuser@example.com', password='newpassword')
    

    @patch('map.views.serialize_bicycle_parking_stands_sdcc')
    @patch('map.views.serialize_dublin_city_parking_stands')
    def test_parking_stands_geojson_view(self, mock_serialize_dcc, mock_serialize_sdcc):
        mock_serialize_sdcc.return_value = {'features': [{'properties': {'location': 'Test Location'}}]}
        mock_serialize_dcc.return_value = {'features': []}
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.parking_stands_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('features', response.data)
        self.assertEqual(response.data['features'][0]['properties']['location'], 'Test Location')
        mock_serialize_sdcc.assert_called_once()
        mock_serialize_dcc.assert_called_once()

    @patch('map.views.Profile.objects.get_or_create')
    def test_user_location_view(self, mock_get_or_create):
        self.profile.location = Point(-6.2603, 53.3498)
        mock_get_or_create.return_value = (self.profile, True)
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.user_location_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('location', response.data)
        self.assertEqual(response.data['location']['latitude'], 53.3498)
        self.assertEqual(response.data['location']['longitude'], -6.2603)
        mock_get_or_create.assert_called_once_with(user=self.user)

    def test_auth_check_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.auth_check_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('authenticated', response.data)
        self.assertTrue(response.data['authenticated'])

    @patch('map.views.fetch_dublin_bikes_geojson')
    def test_dublin_bikes_geojson_view(self, mock_fetch_dublin_bikes_geojson):
        mock_fetch_dublin_bikes_geojson.return_value = {'features': []}
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.dublin_bikes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('features', response.data)
        mock_fetch_dublin_bikes_geojson.assert_called_once()

    @patch('map.views.fetch_general_bikes_geojson')
    def test_bleeper_bikes_geojson_view(self, mock_fetch_general_bikes_geojson):
        mock_fetch_general_bikes_geojson.return_value = {'features': []}
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.bleeper_bikes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('features', response.data)
        mock_fetch_general_bikes_geojson.assert_called_once_with('https://data.smartdublin.ie/bleeperbike-api/bikes/bleeper_bikes/current/bikes.geojson')

    @patch('map.views.fetch_general_bikes_geojson')
    def test_moby_bikes_geojson_view(self, mock_fetch_general_bikes_geojson):
        mock_fetch_general_bikes_geojson.return_value = {'features': []}
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.moby_bikes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('features', response.data)
        mock_fetch_general_bikes_geojson.assert_called_once_with('https://data.smartdublin.ie/mobybikes-api/bikes/mobymoby_dublin/current/bikes.geojson')

    @patch('map.views.serialize_red_cycling_infrastructure')
    def test_red_cycling_geojson_view(self, mock_serialize_red_cycling_infrastructure):
        mock_serialize_red_cycling_infrastructure.return_value = {'features': []}
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.red_cycling_geojson_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('features', response.data)
        mock_serialize_red_cycling_infrastructure.assert_called_once()

    @patch('map.views.serialize_yellow_cycling_infrastructure')
    def test_yellow_cycling_geojson_view(self, mock_serialize_yellow_cycling_infrastructure):
        mock_serialize_yellow_cycling_infrastructure.return_value = {'features': []}
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.yellow_cycling_geojson_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('features', response.data)
        mock_serialize_yellow_cycling_infrastructure.assert_called_once()
        
        
    @patch('map.views.serialize_cycleways_dublin_metro')
    def test_cycleways_geojson_view(self, mock_serialize_cycleways_dublin_metro):
        mock_serialize_cycleways_dublin_metro.return_value = {'features': []}
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.cycleways_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('features', response.data)
        mock_serialize_cycleways_dublin_metro.assert_called_once()
        
    @patch('map.views.serialize_bike_maintenance_stands_dlr')
    def test_maintenance_stands_geojson_view(self, mock_serialize_bike_maintenance_stands_dlr):
        mock_serialize_bike_maintenance_stands_dlr.return_value = {'features': []}
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.maintenance_stands_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('features', response.data)
        mock_serialize_bike_maintenance_stands_dlr.assert_called_once()

