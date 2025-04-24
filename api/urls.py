from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('hotels/', views.list_hotels),
    path('hotels/<int:hotel_id>/floors/', views.list_floors),
    path('floors/<int:floor_id>/rooms/', views.list_rooms),
    path('rooms/<int:room_id>/devices/', views.list_devices_in_room),
    path('rooms/<int:room_id>/fault_status/', views.room_fault_status),

    path('alarms/', views.all_alarms),
    path('alarms/<int:alert_id>/acknowledge/', views.acknowledge_alert, name='acknowledge_alert'),
    path('alarms/<int:alert_id>/dismiss/', views.dismiss_alert, name='dismiss_alert'),

    path('config/fault_detection/', views.get_thresholds),
    path('config/fault_detection/update/', views.update_threshold),

    path('rooms/<str:device_id>/history/', views.room_history),

    path('devices/', views.list_devices),  # GET: List all devices
    path('devices/<str:device_id>/', views.device_detail),  # GET/PUT/DELETE: Device info, update, delete
    path('devices/register/', views.register_device),  # POST: Register new device

    path('users/', views.list_users),  # GET: List users
    path('users/<int:user_id>/', views.user_detail),  # GET/PUT/DELETE
    path('roles/', views.list_roles),  # GET: List all roles
    path('roles/<int:role_id>/permissions/', views.role_permissions),  # GET/POST: View/set role permissions
    path('users/<int:user_id>/assign_role/', views.assign_role),  # POST: Assign role to user

    path('analytics/overview/', views.dashboard_overview),  # GET: Summary of key stats
    path('analytics/faults_by_hotel/', views.faults_by_hotel),  # GET: Fault count per hotel
    path('analytics/faults_over_time/', views.faults_over_time),  # GET: Time series data
    path('analytics/active_alarms/', views.active_alarms_count),  # GET: Count of current alarms
]
# This code defines the URL patterns for the API. Each path corresponds to a view function that handles requests to that endpoint.
# The urlpatterns list is used by Django to route incoming requests to the appropriate view based on the URL.