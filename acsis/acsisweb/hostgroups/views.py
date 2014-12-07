from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import HostGroup
from .serializers import HostGroupSerializer
from hosts.views import JSONResponse


@api_view(['GET', 'POST'])
@csrf_exempt
def hostgroup_list(request):
    """
    List all hostgroups, or create a new hostgroup (or update existing one).
    """
    if request.method == 'GET':
        hosts = HostGroup.objects.all()
        serializer = HostGroupSerializer(hosts, many=True)
#        return JSONResponse(serializer.data)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer_all = HostGroupSerializer(data=data, many=True)

        hostgroupnames = []
        for item in data:
            hostgroupname = item['hostgroup']
            try:
                ### update
                hostgroup = HostGroup.objects.get(hostgroup=hostgroupname)
                serializer = HostGroupSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                hostgroupnames.append(hostgroupname)
            except HostGroup.DoesNotExist:
                ### create
                serializer = HostGroupSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                hostgroupnames.append(hostgroupname)
        if len(data) and not len(hostgroupnames):
            return JSONResponse(serializer.errors, status=400)
        else:
            return JSONResponse(hostgroupnames, status=200)
    else:
        return JSONResponse(serializer.errors, status=400)



def hostgroups_index(request):
    data = {
        'data': HostGroup.objects.all()
    }
    return render_to_response('hostgroups/hostgroups_index.html', data, RequestContext(request))


