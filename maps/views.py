from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
# Create your views here.

from django.db.models import Q
from django.contrib.gis.geos import  Point, Polygon
from django.db import connection
import json 
from maps.models import Site, TimeSeries

def index(request):
    template = loader.get_template('maps/gmap.html')
    context = RequestContext(request, {
        'latest_question_list': 'asd',
    })
    return HttpResponse(template.render(context))


def olindex(request):
    template = loader.get_template('maps/map.html')
    context = RequestContext(request, {
        'latest_question_list': 'asd',
    })
    return HttpResponse(template.render(context))

def clusters(request):
    sites = Site.objects.all().exclude(Q(point__bboverlaps=Point(0,0))|Q(point__isnull=True))
    bbox = [-97.50174285888671,34.981290173471472, -97.017657775878893, 35.31815080315431]
    if bbox:
        bb = [float(x) for x in bbox]
        poly = Polygon.from_bbox(bb)
        x_size = abs(bb[2] - bb[0])/50.0;
        y_size = x_size / 1.5
        sites = sites.filter(point__bboverlaps=poly)

    else:
        x_size = 22.25
        y_size = 11.125
    x_size = 0.02
    y_size = 0.02
    #QuerySet internals, could break on upgrade
    where = '1=1 and '+str(sites.query).split('WHERE')[1]
    sql ='''SELECT min(maps_site.id) as ids,
                  COUNT( maps_site.point ) AS count,
                  ST_SnapToGrid(maps_site.point, %s, %s) as cluster,
                  ST_AsKML(ST_Centroid(ST_Collect(point))) as point
            FROM maps_site WHERE %s
            GROUP BY cluster
            ORDER BY count DESC;''' % (x_size, y_size,where)
    cursor = connection.cursor()
    cursor.execute(sql)
    list_ret = []
    for row in cursor.fetchall():
        # asd = row
        # asds = aaa
        ids, count, cluster, point = row
        list_ret += [{'id':  ids,
                     'count':count,
                     'cluster_id':cluster,
                     'point':point,
                    }]
    return HttpResponse(json.dumps({'data':list_ret,'sql':sql}))

def get_site_data(request,site_id):
    try:
        site = Site.objects.get(id=site_id)
        ts = TimeSeries.objects.filter(site=site).order_by('datetime')

        ts=[{ 'datetime':str(obs.datetime),'data':obs.data} for obs in ts]
        return HttpResponse(json.dumps({'site_id':site_id,'site_name':site.name,'data':ts}))
    except Exception, e:
        return HttpResponse(json.dumps({'error':'Unexpected error happened','msg':e.message}))