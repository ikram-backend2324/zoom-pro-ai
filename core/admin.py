from django.contrib import admin
from .models import Room, Participant

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'host_name', 'is_active', 'created_at', 'participant_count']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'host_name']
    readonly_fields = ['code', 'created_at']

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['name', 'room', 'joined_at', 'is_active']
    list_filter = ['is_active']
