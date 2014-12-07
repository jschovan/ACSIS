from django.db import models
from rest_framework import serializers
from .models import Host

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        compulsory_fields = ['hostname']
        fields = ('hostname', 'aidump_recordversion', 'app_alarmed', 'appstate', \
                  'availability_zone', 'arch', 'cern_os_tenant', 'cnames', 'comment', \
                  'environment', 'fename', 'hwcores', 'hwdisks', 'hwmemory', \
                  'hwswap', 'hwtype', 'hostgroup', 'hw_alarmed', 'ipaddress', \
                  'ipdomain', 'kernel', 'landb_location', 'landb_rackname', \
                  'landb_service_name', 'landbsets', 'lastreport', 'lbaliases', \
                  'location_name', 'lsbdistrelease', 'nc_alarmed', 'os', \
                  'responsible', 'flavour', \
        )


    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(HostSerializer, self).__init__(*args, **kwargs)


    def validate(self, attrs):
        """
            Check that the self.Meta.compulsory_fields are present.
        
        """
        for field in self.Meta.compulsory_fields:
            try:
                if not len(attrs[field]) > 0:
                    raise serializers.ValidationError("%s must not be empty!" % field)
            except KeyError:
                raise serializers.ValidationError("%s must be filled!" % field)
            return attrs


    def create(self, validated_data):
        return Host(**validated_data)


#    def update(self, instance, validated_data):
#        instance.aidump_recordversion = validated_data.get('aidump_recordversion', instance.aidump_recordversion)
#        instance.app_alarmed = validated_data.get('app_alarmed', instance.app_alarmed)
#        instance.appstate = validated_data.get('appstate', instance.appstate)
#        instance.arch = validated_data.get('arch', instance.arch)
#        instance.cern_os_tenant = validated_data.get('cern_os_tenant', instance.cern_os_tenant)
#        instance.cnames = validated_data.get('cnames', instance.cnames)
#        instance.comment = validated_data.get('comment', instance.comment)
#        instance.environment = validated_data.get('environment', instance.environment)
#        instance.fename = validated_data.get('fename', instance.fename)
#        instance.hwcores = validated_data.get('hwcores', instance.hwcores)
#        instance.hwdisks = validated_data.get('hwdisks', instance.hwdisks)
#        instance.hwmemory = validated_data.get('hwmemory', instance.hwmemory)
#        instance.hwswap = validated_data.get('hwswap', instance.hwswap)
#        instance.hwtype = validated_data.get('hwtype', instance.hwtype)
#        instance.hostgroupid = validated_data.get('hostgroupid', instance.hostgroupid)
#        instance.hw_alarmed = validated_data.get('hw_alarmed', instance.hw_alarmed)
#        instance.ipaddress = validated_data.get('ipaddress', instance.ipaddress)
#        instance.ipdomain = validated_data.get('ipdomain', instance.ipdomain)
#        instance.kernel = validated_data.get('kernel', instance.kernel)
#        instance.landb_location = validated_data.get('landb_location', instance.landb_location)
#        instance.landb_rackname = validated_data.get('landb_rackname', instance.landb_rackname)
#        instance.landb_service_name = validated_data.get('landb_service_name', instance.landb_service_name)
#        instance.landbsets = validated_data.get('landbsets', instance.landbsets)
#        instance.lastreport = validated_data.get('lastreport', instance.lastreport)
#        instance.lbaliases = validated_data.get('lbaliases', instance.lbaliases)
#        instance.location_name = validated_data.get('location_name', instance.location_name)
#        instance.lsbdistrelease = validated_data.get('lsbdistrelease', instance.lsbdistrelease)
#        instance.nc_alarmed = validated_data.get('nc_alarmed', instance.nc_alarmed)
#        instance.os = validated_data.get('os', instance.os)
#        instance.responsible = validated_data.get('responsible', instance.responsible)
#        return instance


