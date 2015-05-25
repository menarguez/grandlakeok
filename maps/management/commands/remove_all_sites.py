
from django.core.management.base import BaseCommand, CommandError
from maps.models import Site, TimeSeries
import random
from django.contrib.gis.geos import Point, fromstr 

class Command(BaseCommand):
    help = 'Adds n random sites to the Sites id within a region'

    def add_arguments(self, parser):
        # parser.add_argument('nsites', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        Site.objects.all().delete()
        TimeSeries.objects.all().delete()