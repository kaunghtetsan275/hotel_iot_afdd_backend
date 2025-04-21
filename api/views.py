import requests
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Hotel, Floor, Room, Device, FaultStatus, FaultThreshold
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms.models import model_to_dict
from decouple import config
import psycopg2
from .config.supabase_client import SUPABASE_URL, SUPABASE_API_KEY, HEADERS

class TimescaleDBConnector:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=config('TIMESCALEDB_DATABASE'),
            user=config('TIMESCALEDB_USER'),
            password=config('TIMESCALEDB_PASSWORD'),
            host=config('TIMESCALEDB_HOST'),
            port=config('TIMESCALEDB_PORT')
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

def load_all_supabase():
    # Load hotels
    hotel_url = f"{SUPABASE_URL}/rest/v1/hotels"
    hotel_response = requests.get(hotel_url, headers=HEADERS)
    if hotel_response.status_code == 200:
        hotels = hotel_response.json()
        for item in hotels:
            Hotel.objects.update_or_create(
                id=item["id"],
                defaults={
                    "name": item.get("name", ""),
                    "code": item.get("code")
                }
            )

    # Load floors
    floor_url = f"{SUPABASE_URL}/rest/v1/floors"
    floor_response = requests.get(floor_url, headers=HEADERS)
    if floor_response.status_code == 200:
        floors = floor_response.json()
        for item in floors:
            Floor.objects.update_or_create(
                id=item["id"],
                defaults={
                    "hotel_id": item.get("hotel_id"),
                    "floor_id": item.get("floor_id")
                }
            )

    # Load rooms
    room_url = f"{SUPABASE_URL}/rest/v1/rooms"
    room_response = requests.get(room_url, headers=HEADERS)
    if room_response.status_code == 200:
        rooms = room_response.json()
        for item in rooms:
            Room.objects.update_or_create(
                id=item["id"],
                defaults={
                    "name": item.get("name", ""),
                    "room_number": item.get("room_number"),
                    "floor_id": item.get("floor_id")
                }
            )

    # Load devices
    device_url = f"{SUPABASE_URL}/rest/v1/devices"
    device_response = requests.get(device_url, headers=HEADERS)
    if device_response.status_code == 200:
        devices = device_response.json()
        for item in devices:
            Device.objects.update_or_create(
                id=item["id"],
                defaults={
                    "room_id": item.get("room_id"),
                    "device_identifier": item.get("device_identifier", ""),
                    "sensor_type": item.get("sensor_type", "")
                }
            )

@api_view(['GET'])
def list_hotels(request):
    # list hotel from supabase
    url = f"{SUPABASE_URL}/rest/v1/hotels"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch hotels"}, status=response.status_code)
    hotels = response.json()

    # Query local DB and return serialized data
    hotels = Hotel.objects.all()
    serializer = HotelSerializer(hotels, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_floors(request, hotel_id):
    url = f"{SUPABASE_URL}/rest/v1/floors?hotel_id=eq.{hotel_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch floors"}, status=response.status_code)
    floors = Floor.objects.filter(hotel_id=hotel_id)
    serializer = FloorSerializer(floors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_rooms(request, floor_id):
    url = f"{SUPABASE_URL}/rest/v1/rooms?floor_id=eq.{floor_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch rooms"}, status=response.status_code)
    rooms = Room.objects.filter(floor_id=floor_id)
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def list_devices(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def room_fault_status(request, room_id):
    try:
        devices_url = f"{SUPABASE_URL}/rest/v1/devices?room_id=eq.{room_id}&select=id"
        devices_resp = requests.get(devices_url, headers=HEADERS)
        devices = devices_resp.json()

        device_ids = [d["id"] for d in devices]

        if device_ids:
            # Build the filter like: device_id=in.(1,2,3)
            device_id_filter = ",".join(map(str, device_ids))
            fault_url = f"{SUPABASE_URL}/rest/v1/fault_status?did=in.({device_id_filter})"
            fault_resp = requests.get(fault_url, headers=HEADERS)
            faults_data = fault_resp.json()
            return JsonResponse(faults_data, safe=False)

            # # Upsert into Django DB
            # for item in faults_data:
            #     FaultStatus.objects.update_or_create(
            #         id=item["id"],
            #         defaults={
            #             "device_id": item.get("device_id"),
            #             "fault_type": item.get("fault_type"),
            #             "status": item.get("status"),
            #             "message": item.get("message"),
            #             "detected_at": item.get("detected_at"),
            #             "timestamp": item.get("timestamp"),
            #             "did": item.get("did")
            #         }
            #     )
            # faults = FaultStatus.objects.filter(did__in=device_ids)
            # serializer = FaultStatusSerializer(faults, many=True)
            # return Response(serializer.data)    
            
    except Exception as e:
        return JsonResponse({"Failed to fetch fault status": str(e)}, status=500)

@api_view(['GET'])
def all_alarms(request):
    # get all faulty devices from supabase fault_status table
    url = f"{SUPABASE_URL}/rest/v1/fault_status"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch alarms"}, status=response.status_code)
    alarms = response.json()
    return JsonResponse(alarms, safe=False)

def room_history(request, device_id):
    # Fetch data from TimescaleDB
    cursor = TimescaleDBConnector().conn.cursor()
    cursor.execute("""
        SELECT to_char(datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"'), datapoint, value
        FROM raw_data
        WHERE did = %s
        ORDER BY datetime DESC
        LIMIT 1000
    """, [device_id])
    rows = cursor.fetchall()
    # close the cursor and connection
    cursor.close()
    TimescaleDBConnector().conn.close()
    return JsonResponse(rows, safe=False)

@api_view(['POST'])
def acknowledge_alarm(request, alarm_id):
    try:
        FaultStatus = FaultStatus.objects.get(pk=alarm_id)
        FaultStatus.acknowledged = True
        FaultStatus.save()
        return Response({'status': 'acknowledged'})
    except FaultStatus.DoesNotExist:
        return Response({'error': 'FaultStatus not found'}, status=404)

@api_view(['POST'])
def acknowledge_alert(request, alert_id):
    res = update_alert_status(alert_id, "acknowledged")
    if res.status_code != 200:
        return JsonResponse({"error": "Failed to update alert status"}, status=res.status_code)
    if res.status_code == 204:
        return JsonResponse({"result": "acknowledged", "supabase_response": {}})
    return JsonResponse({"result": "acknowledged", "supabase_response": res.json()})

@api_view(['POST'])
def dismiss_alert(request, alert_id):
    res = update_alert_status(alert_id, "dismissed")
    if res.status_code != 200:
        return JsonResponse({"error": "Failed to update alert status"}, status=res.status_code)
    if res.status_code == 204:
        return JsonResponse({"result": "dismissed", "supabase_response": {}})
    return JsonResponse({"result": "dismissed", "supabase_response": res.json()})

def update_alert_status(alert_id, status):
    url = f"{SUPABASE_URL}/rest/v1/realtime_alerts?id=eq.{alert_id}"
    payload = {"status": status}
    response = requests.patch(url, headers=HEADERS, json=payload)
    return response

# GET all thresholds grouped by sensor type
@api_view(['GET', 'PUT'])
def get_thresholds(request):
    try:
        # Assuming you have a single record for thresholds
        threshold = FaultThreshold.objects.first()
        
        if request.method == 'GET':
            serializer = FaultThresholdSerializer(threshold)
            return Response(serializer.data)
            
        elif request.method == 'PUT':
            serializer = FaultThresholdSerializer(threshold, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# POST or PUT to update a specific threshold (or create one if it doesn't exist)
@csrf_exempt
def update_threshold(request):
    if request.method in ['POST', 'PUT']:
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Debugging line
            threshold, created = FaultThreshold.objects.get_or_create(
                id=data.get('id', None),  # Assuming you have an ID to identify the threshold
                defaults={
                    'temperature_min': data.get('temperature_min', None),
                    'temperature_max': data.get('temperature_max', None),
                    'humidity_min': data.get('humidity_min', None),
                    'humidity_max': data.get('humidity_max', None),
                    'co2_min': data.get('co2_min', None),
                    'co2_max': data.get('co2_max', None),
                    'power_kw_min': data.get('power_kw_min', None),
                    'power_kw_max': data.get('power_kw_max', None),
                    'occupancy_required': data.get('occupancy_required', False),
                    'sensor_online_required': data.get('sensor_online_required', True),
                    'sensitivity_min': data.get('sensitivity_min', None),
                    'sensitivity_max': data.get('sensitivity_max', None)
                }
            )

            # Update fields
            for field in [
                'temperature_min', 'temperature_max', 'humidity_min', 'humidity_max',
                'co2_min', 'co2_max','power_kw_min', 'power_kw_max','occupancy_required',
                'sensor_online_required', 'sensitivity_min', 'sensitivity_max'
            ]:
                if field in data:
                    setattr(threshold, field, data[field])

            threshold.save()
            return JsonResponse(model_to_dict(threshold), status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
@require_http_methods(["GET", "PUT", "DELETE"])
def device_detail(request, device_id):
    if request.method == "GET":
        # TODO: Fetch specific device
        return JsonResponse({"device_id": device_id})
    elif request.method == "PUT":
        data = json.loads(request.body)
        # TODO: Update device
        return JsonResponse({"message": "Device updated"})
    elif request.method == "DELETE":
        # TODO: Delete device
        return JsonResponse({"message": "Device deleted"})

@require_http_methods(["POST"])
def register_device(request):
    data = json.loads(request.body)
    # TODO: Register a new device
    return JsonResponse({"message": "Device registered"}, status=201)

@require_http_methods(["GET"])
def list_users(request):
    # TODO: Fetch users
    return JsonResponse({"users": []})

@require_http_methods(["GET", "PUT", "DELETE"])
def user_detail(request, user_id):
    if request.method == "GET":
        # TODO: Fetch user
        return JsonResponse({"user_id": user_id})
    elif request.method == "PUT":
        data = json.loads(request.body)
        # TODO: Update user
        return JsonResponse({"message": "User updated"})
    elif request.method == "DELETE":
        # TODO: Delete user
        return JsonResponse({"message": "User deleted"})

@require_http_methods(["GET"])
def list_roles(request):
    # TODO: List roles
    return JsonResponse({"roles": []})

@require_http_methods(["GET", "POST"])
def role_permissions(request, role_id):
    if request.method == "GET":
        # TODO: Get permissions for role
        return JsonResponse({"role_id": role_id, "permissions": []})
    elif request.method == "POST":
        data = json.loads(request.body)
        # TODO: Update permissions
        return JsonResponse({"message": "Permissions updated"})

@require_http_methods(["POST"])
def assign_role(request, user_id):
    data = json.loads(request.body)
    # TODO: Assign role to user
    return JsonResponse({"message": "Role assigned"})

@require_http_methods(["GET"])
def dashboard_overview(request):
    # TODO: Return key summary data
    return JsonResponse({"summary": {}})

@require_http_methods(["GET"])
def faults_by_hotel(request):
    # TODO: Return faults grouped by hotel
    return JsonResponse({"faults_by_hotel": []})

@require_http_methods(["GET"])
def faults_over_time(request):
    # TODO: Return time series fault data
    return JsonResponse({"time_series": []})

@require_http_methods(["GET"])
def active_alarms_count(request):
    # TODO: Return count of active alarms
    return JsonResponse({"active_alarms": 0})