from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from ..models import Hotel, Floor, Room, Device, FaultStatus, FaultThreshold
from ..config.supabase_client import supabase

@receiver(post_save, sender=Hotel)
def sync_hotel_to_supabase_on_save(sender, instance, created, **kwargs):
    payload = {
        "id": instance.id,
        "name": instance.name,
        "code": instance.code,
    }

    if created:
        # INSERT to Supabase
        table_exists = supabase.table("hotels").select("*").limit(1).execute()
        if not table_exists:
            print("Table 'hotels' does not exist in Supabase.")
        else:
            existing_record = supabase.table("hotels").select("id").eq("id", instance.id).execute()
            if not existing_record.data:
                supabase.table("hotels").insert(payload).execute()
    else:
        # UPDATE Supabase — assumes id is the unique identifier
        table_exists = supabase.table("hotels").select("*").limit(1).execute()
        if not table_exists:
            print("Table 'hotels' does not exist in Supabase.")
        else:
            existing_record = supabase.table("hotels").select("id").eq("id", instance.id).execute()
            if existing_record.data:
                supabase.table("hotels").update(payload).eq("id", instance.id).execute()

@receiver(post_delete, sender=Hotel)
def sync_hotel_to_supabase_on_delete(sender, instance, **kwargs):
    # DELETE from Supabase
    table_exists = supabase.table("hotels").select("*").limit(1).execute()
    if not table_exists:
        print("Table 'hotels' does not exist in Supabase.")
    else:
        existing_record = supabase.table("hotels").select("id").eq("id", instance.id).execute()
        if existing_record.data:
            supabase.table("hotels").delete().eq("id", instance.id).execute()

@receiver(post_save, sender=Floor)
def sync_floor_to_supabase_on_save(sender, instance, created, **kwargs):
    payload = {
        "id": instance.id,
        "hotel_id": instance.hotel_id.id if instance.hotel_id else None,
        "floor_id": instance.floor_id,
    }

    if created:
        table_exists = supabase.table("floors").select("*").limit(1).execute()
        if not table_exists:
            print("Table 'floors' does not exist in Supabase.")
        else:
            existing_record = supabase.table("floors").select("id").eq("id", instance.id).execute()
            if not existing_record.data:
                supabase.table("floors").insert(payload).execute()
    else:
        table_exists = supabase.table("floors").select("*").limit(1).execute()
        if not table_exists:
            print("Table 'floors' does not exist in Supabase.")
        else:
            existing_record = supabase.table("floors").select("id").eq("id", instance.id).execute()
            if existing_record.data:
                supabase.table("floors").update(payload).eq("id", instance.id).execute()

@receiver(post_delete, sender=Floor)
def sync_floor_to_supabase_on_delete(sender, instance, **kwargs):
    table_exists = supabase.table("floors").select("*").limit(1).execute()
    if not table_exists:
        print("Table 'floors' does not exist in Supabase.")
    else:
        existing_record = supabase.table("floors").select("id").eq("id", instance.id).execute()
        if existing_record.data:
            supabase.table("floors").delete().eq("id", instance.id).execute()

@receiver(post_save, sender=Room)
def sync_room_to_supabase_on_save(sender, instance, created, **kwargs):
    payload = {
        "id": instance.id,
        "name": instance.name,
        "room_number": instance.room_number,
        "floor_id": instance.floor.id if instance.floor else None,
    }

    if created:
        table_exists = supabase.table("rooms").select("*").limit(1).execute()
        if not table_exists:
            print("Table 'rooms' does not exist in Supabase.")
        else:
            existing_record = supabase.table("rooms").select("id").eq("id", instance.id).execute()
            if not existing_record.data:
                supabase.table("rooms").insert(payload).execute()
    else:
        table_exists = supabase.table("rooms").select("*").limit(1).execute()
        if not table_exists:
            print("Table 'rooms' does not exist in Supabase.")
        else:
            existing_record = supabase.table("rooms").select("id").eq("id", instance.id).execute()
            if existing_record.data:
                supabase.table("rooms").update(payload).eq("id", instance.id).execute()

@receiver(post_delete, sender=Room)
def sync_room_to_supabase_on_delete(sender, instance, **kwargs):
    table_exists = supabase.table("rooms").select("*").limit(1).execute()
    if not table_exists:
        print("Table 'rooms' does not exist in Supabase.")
    else:
        existing_record = supabase.table("rooms").select("id").eq("id", instance.id).execute()
        if existing_record.data:
            supabase.table("rooms").delete().eq("id", instance.id).execute()

@receiver(post_save, sender=Device)
def sync_device_to_supabase_on_save(sender, instance, created, **kwargs):
    payload = {
        "id": instance.id,
        "room_id": instance.room.id if instance.room else None,
        "device_identifier": instance.device_identifier,
        "sensor_type": instance.sensor_type,
    }

    if created:
        table_exists = supabase.table("devices").select("*").limit(1).execute()
        if not table_exists:
            print("Table 'devices' does not exist in Supabase.")
        else:
            existing_record = supabase.table("devices").select("id").eq("id", instance.id).execute()
            if not existing_record.data:
                supabase.table("devices").insert(payload).execute()
    else:
        table_exists = supabase.table("devices").select("*").limit(1).execute()
        if not table_exists:
            print("Table 'devices' does not exist in Supabase.")
        else:
            existing_record = supabase.table("devices").select("id").eq("id", instance.id).execute()
            if existing_record.data:
                supabase.table("devices").update(payload).eq("id", instance.id).execute()

@receiver(post_delete, sender=Device)
def sync_device_to_supabase_on_delete(sender, instance, **kwargs):
    table_exists = supabase.table("devices").select("*").limit(1).execute()
    if not table_exists:
        print("Table 'devices' does not exist in Supabase.")
    else:
        existing_record = supabase.table("devices").select("id").eq("id", instance.id).execute()
        if existing_record.data:
            supabase.table("devices").delete().eq("id", instance.id).execute()

@receiver(post_save, sender=FaultStatus)
def sync_fault_status_to_supabase_on_save(sender, instance, created, **kwargs):
    payload = {
        "id": instance.id,
        "device_id": instance.device_id,
        "status": instance.status,
        "timestamp": instance.timestamp,
    }

    if created:
        table_exists = supabase.table("fault_statuses").select("*").limit(1).execute()
        if not table_exists:
            print("Table 'fault_statuses' does not exist in Supabase.")
        else:
            existing_record = supabase.table("fault_statuses").select("id").eq("id", instance.id).execute()
            if not existing_record.data:
                supabase.table("fault_statuses").insert(payload).execute()
    else:
        table_exists = supabase.table("fault_statuses").select("*").limit(1).execute()
        if not table_exists:
            print("Table 'fault_statuses' does not exist in Supabase.")
        else:
            existing_record = supabase.table("fault_statuses").select("id").eq("id", instance.id).execute()
            if existing_record.data:
                supabase.table("fault_statuses").update(payload).eq("id", instance.id).execute()

@receiver(post_delete, sender=FaultStatus)
def sync_fault_status_to_supabase_on_delete(sender, instance, **kwargs):
    table_exists = supabase.table("fault_statuses").select("*").limit(1).execute()
    if not table_exists:
        print("Table 'fault_statuses' does not exist in Supabase.")
    else:
        existing_record = supabase.table("fault_statuses").select("id").eq("id", instance.id).execute()
        if existing_record.data:
            supabase.table("fault_statuses").delete().eq("id", instance.id).execute()

@receiver(post_save, sender=FaultThreshold)
def sync_fault_threshold_to_supabase_on_save(sender, instance, created, **kwargs):
    payload = {
        "id": instance.id,
        "device_id": instance.device_id,
        "threshold": instance.threshold,
        "timestamp": instance.timestamp,
    }

    if created:
        table_exists = supabase.table("fault_thresholds").select("*").limit(1).execute()
        if not table_exists:
            print("Table 'fault_thresholds' does not exist in Supabase.")
        else:
            existing_record = supabase.table("fault_thresholds").select("id").eq("id", instance.id).execute()
            if not existing_record.data:
                supabase.table("fault_thresholds").insert(payload).execute()
    else:
        table_exists = supabase.table("fault_thresholds").select("*").limit(1).execute()
        if not table_exists:
            print("Table 'fault_thresholds' does not exist in Supabase.")
        else:
            existing_record = supabase.table("fault_thresholds").select("id").eq("id", instance.id).execute()
            if existing_record.data:
                supabase.table("fault_thresholds").update(payload).eq("id", instance.id).execute()

@receiver(post_delete, sender=FaultThreshold)
def sync_fault_threshold_to_supabase_on_delete(sender, instance, **kwargs):
    table_exists = supabase.table("fault_thresholds").select("*").limit(1).execute()
    if not table_exists:
        print("Table 'fault_thresholds' does not exist in Supabase.")
    else:
        existing_record = supabase.table("fault_thresholds").select("id").eq("id", instance.id).execute()
        if existing_record.data:
            supabase.table("fault_thresholds").delete().eq("id", instance.id).execute()
