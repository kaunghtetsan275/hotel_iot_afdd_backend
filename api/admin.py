from django.contrib import admin

# Register your models here.
from .models import Hotel, Floor, Room, Device, FaultStatus, FaultThreshold

admin.site.register(Hotel)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Device)
admin.site.register(FaultStatus)
admin.site.register(FaultThreshold)
