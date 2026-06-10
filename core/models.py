from django.db import models
import random
import string


def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))


class Room(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=9, unique=True, default=generate_room_code)
    password = models.CharField(max_length=100, blank=True, null=True)
    host_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def participant_count(self):
        return self.participants.filter(is_active=True).count()

    @property
    def has_password(self):
        return bool(self.password)


class Participant(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=100)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} in {self.room.name}"
