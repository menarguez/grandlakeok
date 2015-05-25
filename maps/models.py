# from django.db import models
from django.contrib.gis.db import models

class Site(models.Model):
    name = models.CharField(max_length=50)
    data = models.FloatField(default=0.0)

    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    point = models.PointField(srid=4326,help_text="Represented as (longitude, latitude)")
    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return self.name

class TimeSeries(models.Model):
    site = models.ForeignKey(Site, null=False)
    datetime = models.DateTimeField(null=False)
    data = models.FloatField(null=False)

    class __meta__:
        unique_together = (("site", "datetime"),)
# Create your models here.
