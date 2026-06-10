from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Room, Participant


SEED_ROOMS = [
    {
        "name": "Morning Standup",
        "host_name": "Alex",
        "description": "Daily team sync — all devs welcome",
        "password": "",
        "participants": ["Alex", "Emma", "Chris"],
    },
    {
        "name": "Design Review Q4",
        "host_name": "Sara",
        "description": "Reviewing the new landing page designs",
        "password": "design24",
        "participants": ["Sara", "Liu"],
    },
    {
        "name": "Open Study Hall",
        "host_name": "Mike",
        "description": "Open room for anyone to join and study together",
        "password": "",
        "participants": ["Mike", "Nadia", "Tom", "Priya"],
    },
    {
        "name": "Product Demo",
        "host_name": "Jordan",
        "description": "Live walkthrough of the latest features",
        "password": "",
        "participants": ["Jordan", "Casey"],
    },
]


class Command(BaseCommand):
    help = "Seed the database with demo rooms and participants"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["clear"]:
            Room.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing rooms."))

        if Room.objects.exists():
            self.stdout.write(self.style.NOTICE("Database already has rooms — skipping seed. Use --clear to reseed."))
            return

        created_rooms = []
        for data in SEED_ROOMS:
            room = Room.objects.create(
                name=data["name"],
                host_name=data["host_name"],
                description=data["description"],
                password=data["password"] or None,
            )
            for pname in data["participants"]:
                Participant.objects.create(room=room, name=pname)
            created_rooms.append(room)
            self.stdout.write(
                self.style.SUCCESS(
                    f"  ✓ {room.name}  [{room.code}]  "
                    f"{'🔒 Private' if room.has_password else '🌐 Open'}  "
                    f"— {room.participant_count} participants"
                )
            )

        self.stdout.write(self.style.SUCCESS(f"\nSeeded {len(created_rooms)} rooms successfully."))
