from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Hotel, Floor, Room, FaultStatus, FaultThreshold

class APITestCase(TestCase):
    def setUp(self):
        # Set up test data and API client
        self.client = APIClient()
        self.hotel = Hotel.objects.create(id=1, name="Test Hotel", code="TH001")
        self.floor = Floor.objects.create(id=1, hotel_id=self.hotel, floor_id="F1")  # Use the Hotel instance
        self.room = Room.objects.create(id=1, name="Room 101", room_number="101", floor=self.floor)  # Use the Floor instance
        self.device = FaultStatus.objects.create(id=1, device_id=1, fault_type="Test Fault", status="active")
        self.threshold = FaultThreshold.objects.create(temperature_min=20, temperature_max=30)

    def test_list_hotels(self):
        response = self.client.get('/hotels/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_floors(self):
        response = self.client.get(f'/hotels/{self.hotel.id}/floors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_rooms(self):
        response = self.client.get(f'/floors/{self.floor.id}/rooms/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_room_fault_status(self):
        response = self.client.get(f'/rooms/{self.room.id}/fault_status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_alarms(self):
        response = self.client.get('/alarms/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_room_history(self):
        response = self.client.get(f'/rooms/{self.device.device_id}/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Uncomment and update additional tests as needed
    # def test_acknowledge_alert(self):
    #     response = self.client.post(f'/alarms/{self.device.id}/acknowledge/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_dismiss_alert(self):
    #     response = self.client.post(f'/alarms/{self.device.id}/dismiss/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_thresholds(self):
    #     response = self.client.get('/config/fault_detection/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_threshold(self):
    #     payload = {
    #         "temperature_min": 18,
    #         "temperature_max": 28
    #     }
    #     response = self.client.put('/config/fault_detection/update/', payload, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_list_devices(self):
    #     response = self.client.get('/devices/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_device_detail(self):
    #     response = self.client.get(f'/devices/{self.device.device_id}/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_register_device(self):
    #     payload = {
    #         "device_id": 2,
    #         "name": "New Device"
    #     }
    #     response = self.client.post('/devices/register/', payload, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_list_users(self):
    #     response = self.client.get('/users/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_user_detail(self):
    #     response = self.client.get('/users/1/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_list_roles(self):
    #     response = self.client.get('/roles/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_role_permissions(self):
    #     response = self.client.get('/roles/1/permissions/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_assign_role(self):
    #     payload = {
    #         "role_id": 1,
    #         "user_id": 1
    #     }
    #     response = self.client.post('/users/1/assign_role/', payload, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_dashboard_overview(self):
    #     response = self.client.get('/analytics/overview/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_faults_by_hotel(self):
    #     response = self.client.get('/analytics/faults_by_hotel/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_faults_over_time(self):
    #     response = self.client.get('/analytics/faults_over_time/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_active_alarms_count(self):
    #     response = self.client.get('/analytics/active_alarms/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
