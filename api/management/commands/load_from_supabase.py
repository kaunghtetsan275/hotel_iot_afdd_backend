import os
import requests
from django.core.management.base import BaseCommand
from api.models import Hotel, Floor, Room, Device, FaultThreshold

SUPABASE_URL = os.getenv("SUPABASE_URL")
HEADERS = {
    "apikey": os.getenv("SUPABASE_API_KEY"),
    "Authorization": f"Bearer {os.getenv('SUPABASE_API_KEY')}"
}

class Command(BaseCommand):
    help = "Load data from Supabase into the database"

    def handle(self, *args, **kwargs):
        self.load_all_supabase()

    def load_all_supabase(self):
        # Load hotels
        hotel_url = f"{SUPABASE_URL}/rest/v1/hotels"
        hotel_response = requests.get(hotel_url, headers=HEADERS)
        if hotel_response.status_code == 200:
            hotels = hotel_response.json()
            for item in hotels:
                if not Hotel.objects.filter(id=item["id"]).exists():
                    Hotel.objects.create(
                        id=item["id"],
                        name=item.get("name", ""),
                        code=item.get("code")
                    )

        # Load floors
        floor_url = f"{SUPABASE_URL}/rest/v1/floors"
        floor_response = requests.get(floor_url, headers=HEADERS)
        if floor_response.status_code == 200:
            floors = floor_response.json()
            for item in floors:
                if not Floor.objects.filter(id=item["id"]).exists():
                    Floor.objects.create(
                        id=item["id"],
                        hotel_id=Hotel.objects.get(id=item.get("hotel_id")),
                        floor_id=item.get("floor_id")
                    )

        # Load rooms
        room_url = f"{SUPABASE_URL}/rest/v1/rooms"
        room_response = requests.get(room_url, headers=HEADERS)
        if room_response.status_code == 200:
            rooms = room_response.json()
            for item in rooms:
                if not Room.objects.filter(id=item["id"]).exists():
                    Room.objects.create(
                        id=item["id"],
                        name=item.get("name", ""),
                        room_number=item.get("room_number"),
                        floor=Floor.objects.get(id=item.get("floor_id"))
                    )

        # Load devices
        device_url = f"{SUPABASE_URL}/rest/v1/devices"
        device_response = requests.get(device_url, headers=HEADERS)
        if device_response.status_code == 200:
            devices = device_response.json()
            for item in devices:
                if not Device.objects.filter(id=item["id"]).exists():
                    Device.objects.create(
                        id=item["id"],
                        room=Room.objects.get(id=item.get("room_id")),
                        device_identifier=item.get("device_identifier", ""),
                        sensor_type=item.get("sensor_type", "")
                    )
        
        # Load thresholds
        threshold_url = f"{SUPABASE_URL}/rest/v1/fault_thresholds"
        threshold_response = requests.get(threshold_url, headers=HEADERS)
        if threshold_response.status_code == 200:
            thresholds = threshold_response.json()
            for item in thresholds:
                if not FaultThreshold.objects.filter(id=item["id"]).exists():
                    FaultThreshold.objects.create(
                        id=item["id"],
                        temperature_min=item.get("temperature_min"),
                        temperature_max=item.get("temperature_max"),
                        humidity_min=item.get("humidity_min"),
                        humidity_max=item.get("humidity_max"),
                        co2_min=item.get("co2_min"),
                        co2_max=item.get("co2_max"),
                        power_kw_min=item.get("power_kw_min"),
                        power_kw_max=item.get("power_kw_max"),
                        occupancy_required=item.get("occupancy_required"),
                        sensor_online_required=item.get("sensor_online_required"),
                        sensitivity_min=item.get("sensitivity_min"),
                        sensitivity_max=item.get("sensitivity_max")
                    )
