from django.db import models

class Hotel(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    name = models.CharField(max_length=800)
    code = models.CharField(max_length=800, blank=True, null=True)

    class Meta:
        managed = True 
        db_table = 'hotels'  # matches Supabase table name

class Floor(models.Model):
    id = models.AutoField(primary_key=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    floor_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True 
        db_table = 'floors'

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    room_number = models.TextField(blank=True, null=True)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

    class Meta:
        managed = True 
        db_table = 'rooms'

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    device_identifier = models.TextField(blank=True, null=True)
    sensor_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = True 
        db_table = 'devices'

class FaultStatus(models.Model):
    id = models.BigIntegerField(primary_key=True)
    # device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='fault_statuses')
    device_id = models.TextField()
    fault_type = models.TextField()
    status = models.TextField()
    message = models.TextField(blank=True, null=True)
    detected_at = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    did = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'fault_status'

class FaultThreshold(models.Model):
    # Threshold fields
    id = models.AutoField(primary_key=True)
    temperature_min = models.FloatField(blank=True, null=True)
    temperature_max = models.FloatField(blank=True, null=True)
    humidity_min = models.FloatField(blank=True, null=True)
    humidity_max = models.FloatField(blank=True, null=True)
    co2_min = models.FloatField(blank=True, null=True)
    co2_max = models.FloatField(blank=True, null=True)
    power_kw_min = models.FloatField(blank=True, null=True)
    power_kw_max = models.FloatField(blank=True, null=True)
    occupancy_required = models.BooleanField(default=False)
    sensor_online_required = models.BooleanField(default=True)
    sensitivity_min = models.FloatField(blank=True, null=True)
    sensitivity_max = models.FloatField(blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True 
        db_table = 'fault_thresholds'
