from django.core.management.base import BaseCommand, CommandError
from maps.models import Site,TimeSeries
import random
from django.contrib.gis.geos import Point, fromstr 
from random import gauss
import time
import datetime

class Command(BaseCommand):
    help = 'Adds n random sites to the Sites id within a region'

    def add_arguments(self, parser):
        parser.add_argument('nsites', nargs='+', type=int)

    def generate_random_dist(self, numel,min_num,max_num):
        values = []
        while len(values) < numel:
            value = random.uniform(min_num,max_num)
            values.append(value)
        return values
    def add_random_time_series(self, site):
        numel = 50
        values = sorted(self.generate_random_dist(numel,0,1))
        time_end = round(time.time())
        time_ini = time_end-(numel*60)
        times = [datetime.datetime.fromtimestamp(time_ini+(i*60)) for i in range(0,numel)]
        for i in range(0, len(values)):
            ts = TimeSeries(site = site, datetime=times[i], data = values[i] )
            ts.save()
    def handle(self, *args, **options):
        nsites  = int(options['nsites'][0])
        min_lon = -97.32651
        max_lon = -97.21355
        min_lat = 35.18879
        max_lat = 35.25831 
        for i in range(0,nsites):
            location = [random.uniform(min_lon, max_lon),random.uniform(min_lat, max_lat)]
            print location
            point = fromstr("SRID=4326;POINT(%s %s)" % (location[0], location[1]))
            new_site = Site(name='Site%d'%i,point = point,data=random.uniform(1,100) )
            new_site.save()
            self.add_random_time_series(new_site)

        self.stdout.write('Successfully saved %d sites' % nsites)