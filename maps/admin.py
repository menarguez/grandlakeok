from django.contrib.gis import admin

from .models import Site,TimeSeries


class SiteAdmin(admin.OSMGeoAdmin):
    list_display = ('name','point','data')
    pass

admin.site.register(Site, SiteAdmin)

class TimeSeriesAdmin(admin.OSMGeoAdmin):
    list_display = ('site','datetime','data')
    list_filter = ('site','datetime')
    pass

admin.site.register(TimeSeries, TimeSeriesAdmin)