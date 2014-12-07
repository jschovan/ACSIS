from django.db import models

# Create your models here.

class HostGroup(models.Model):
    hostgroup = models.CharField(max_length=50, db_column='HOSTGROUP', blank=False, null=False, primary_key=True)
    responsible = models.CharField(max_length=50, db_column='RESPONSIBLE', blank=True, null=False)
    services = models.CharField(max_length=5, db_column='SERVICES', blank=True, null=True)

    class Meta:
#        app_label = 'hosts'
        db_table = u'hostgroups'


