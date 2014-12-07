from django.db import models
from hostgroups.models import HostGroup


class Host(models.Model):
#    id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=30, db_column='HOSTNAME', blank=False, null=False, primary_key=True)
    availability_zone = models.CharField(max_length=30, db_column='AVAILABILITY_ZONE', blank=True, null=True)
    aidump_recordversion = models.IntegerField(db_column='AIDUMP_RECORDVERSION', null=True, blank=True)
    app_alarmed = models.BooleanField(null=False, blank=True, default=False, db_column='APP_ALARMED')
    appstate = models.CharField(max_length=15, db_column='APPSTATE', blank=True, null=False)
    arch = models.CharField(max_length=10, db_column='ARCH', blank=True, null=False)
    cern_os_tenant = models.CharField(max_length=30, db_column='CERN_OS_TENANT', blank=True, null=True)
    cnames = models.CharField(max_length=256, db_column='CNAMES', blank=True, null=True)
    comment = models.CharField(max_length=256, db_column='COMMENT', blank=True, null=True)
    environment = models.CharField(max_length=10, db_column='ENVIRONMENT', blank=True, null=True)
    fename = models.CharField(max_length=50, db_column='FENAME', blank=True, null=True)
    flavour = models.CharField(max_length=10, db_column='FLAVOUR', blank=True, null=True)
    hwcores = models.CharField(max_length=3, db_column='HWCORES', blank=True, null=True)
    hwdisks = models.PositiveSmallIntegerField(db_column='HWDISKS', blank=True, null=True)
    hwmemory = models.CharField(max_length=10, db_column='HWMEMORY', blank=True, null=True)
    hwswap = models.CharField(max_length=10, db_column='HWSWAP', blank=True, null=True)
    hwtype = models.CharField(max_length=10, db_column='HWTYPE', blank=True, null=True)
    hostgroup = models.CharField(max_length=50, db_column='HOSTGROUPNAME', blank=False, null=False)
    hw_alarmed = models.BooleanField(null=False, blank=True, default=False, db_column='HW_ALARMED')
    ipaddress = models.CharField(max_length=15, db_column='IPADDRESS', blank=True, null=True)
    ipdomain = models.CharField(max_length=10, db_column='IPDOMAIN', blank=True, null=True)
    kernel = models.CharField(max_length=50, db_column='KERNEL', blank=True, null=True)
    landb_location = models.CharField(max_length=15, db_column='LANDB_LOCATION', blank=True, null=True)
    landb_rackname = models.CharField(max_length=5, db_column='LANDB_RACKNAME', blank=True, null=True)
    landb_service_name = models.CharField(max_length=15, db_column='LANDB_SERVICE_NAME', blank=True, null=True)
    landbsets = models.CharField(max_length=15, db_column='LANDBSETS', blank=True, null=True)
    lastreport = models.DateTimeField(db_column='LASTREPORT', blank=True, null=True)
    lbaliases = models.CharField(max_length=256, db_column='LBALIASES', blank=True, null=True)
    location_name = models.CharField(max_length=50, db_column='LOCATION_NAME', blank=True, null=True)
    lsbdistrelease = models.CharField(max_length=5, db_column='LSBDISTRELEASE', blank=True, null=True)
    nc_alarmed = models.BooleanField(null=False, blank=True, default=False, db_column='NC_ALARMED')
    os = models.CharField(max_length=5, db_column='OS', blank=True, null=True)
    responsible = models.CharField(max_length=50, db_column='RESPONSIBLE', blank=True, null=False)

    class Meta:
#        app_label = 'hosts'
        db_table = u'hosts'
        ordering = ('hostname',)
#        unique_together = ('id', 'hostname',)

