from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import Host
from .serializers import HostSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@api_view(['GET', 'POST'])
@csrf_exempt
def host_list(request):
    """
    List all hosts, or create a new host (or update existing one).
    """
    if request.method == 'GET':
        hosts = Host.objects.all()
        serializer = HostSerializer(hosts, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer_all = HostSerializer(data=data, many=True)

        hostnames = []
        for item in data:
            hostname = item['hostname']
            try:
                ### update
                host = Host.objects.get(hostname=hostname)
                serializer = HostSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                hostnames.append(hostname)
            except Host.DoesNotExist:
                ### create
                serializer = HostSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                hostnames.append(hostname)
        if len(data) and not len(hostnames):
            return JSONResponse(serializer.errors, status=400)
        else:
            return JSONResponse(hostnames, status=200)
    else:
        return JSONResponse(serializer.errors, status=400)


def hosts_index(request):
    data = {
        'data': Host.objects.all().values(\
                'hostname', 'hostgroup', 'responsible',
                'appstate', 'environment',
                'availability_zone', 'flavour',
                'hwcores', 'hwdisks', 'hwmemory', 'hwswap', 'hwtype',
                'arch', 'os', 'lsbdistrelease',
                'lbaliases', 'app_alarmed', 'hw_alarmed', 'nc_alarmed',
#                'arch', 'cern_os_tenant', 'cnames', 'comment', \
#                'environment', 'fename', 'hwcores', 'hwdisks', 'hwmemory', \
#                'hwswap', 'hwtype', 'ipaddress', \
#                  'ipdomain', 'kernel', 'landb_location', 'landb_rackname', \
#                  'landb_service_name', 'landbsets', 'lastreport', 'lbaliases', \
#                  'location_name', 'lsbdistrelease',
#                  'app_alarmed', 'hw_alarmed', 'nc_alarmed', 'os', \
                                        )
    }
    return render_to_response('hosts/hosts_index.html', data, RequestContext(request))
