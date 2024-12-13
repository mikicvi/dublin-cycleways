from django.urls import path
from . import views

urlpatterns = [
    path ('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('offline/', views.offline, name='offline'),
    path('logout/', views.logout_view, name='logout'),
    path('map/', views.map_view, name='map'),
    path('cycleways_geojson/', views.cycleways_geojson, name='cycleways_geojson'),
    # #path('signup/', views.signup_view, name='signup'),
    path('update_location/', views.update_location, name='update_location'),
    path('parking_stands_geojson/', views.parking_stands_geojson, name='parking_stands_geojson'),
    path('maintenance_stands_geojson/', views.maintenance_stands_geojson, name='maintenance_stands_geojson'),
]
