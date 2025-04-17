import os
import requests
from django.core.management.base import BaseCommand
from api.models import Hotel, Floor, Room, Device

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
                        "hotel_id": Hotel.objects.get(id=item.get("hotel_id")),
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
                        "floor": Floor.objects.get(id=item.get("floor_id"))
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
                        "room": Room.objects.get(id=item.get("room_id")),
                        "device_identifier": item.get("device_identifier", ""),
                        "sensor_type": item.get("sensor_type", "")
                    }
                )