from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import Service
from .serializers import ServiceSerializer
from hosts.views import JSONResponse


@api_view(['GET', 'POST'])
@csrf_exempt
def service_list(request):
    """
    List all services, or create a new service (or update existing one).
    """
    if request.method == 'GET':
        hosts = Service.objects.all()
        serializer = ServiceSerializer(hosts, many=True)
#        return JSONResponse(serializer.data)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer_all = ServiceSerializer(data=data, many=True)

        services = []
        for item in data:
            servicename = item['service']
            try:
                ### update
                service = Service.objects.get(service=servicename)
                serializer = ServiceSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                services.append(servicename)
            except Service.DoesNotExist:
                ### create
                serializer = ServiceSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                services.append(servicename)
        if len(data) and not len(services):
            return JSONResponse(serializer.errors, status=400)
        else:
            return JSONResponse(services, status=200)
    else:
        return JSONResponse(serializer.errors, status=400)



def services_index(request):
    data = {
        'data': Service.objects.all(),
    }
    return render_to_response('services/services_index.html', data, RequestContext(request))



