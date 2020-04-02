from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):
    help = "this commands tell hello"

    #     def add_arguments(self, parser):

    #         parser.add_argument(
    #             "--times", help="how many i love you",
    #         )

    def handle(self, *args, **options):
        amenities = [
            "microwave",
            "mirror",
            "air conditioning",
            "alarm clock",
            "balcony",
            "bathroom",
            "bathtub",
            "boating",
            "play ground",
            "towels",
            "TV",
            "queen size bed",
        ]
        for a in amenities:
            Amenity.objects.create(name=a)

        self.stdout.write(self.style.SUCCESS("Amenities okay"))
