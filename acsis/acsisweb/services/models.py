from django.db import models

class Service(models.Model):
    service = models.CharField(max_length=50, db_column='SERVICE', blank=False, null=False)
    description = models.CharField(max_length=256, db_column='DESCRIPTION', blank=True, null=True)
    parents = models.CharField(max_length=256, db_column='PARENTS', blank=True, null=True)
    doccard = models.URLField(db_column='DOCCARD', blank=True, null=True)
    contacts = models.CharField(max_length=256, db_column='CONTACTS', blank=True, null=True)
    criticality = models.CharField(max_length=10, db_column='CRITICALITY', blank=True, null=True)
    allowed_downtime = models.PositiveSmallIntegerField(db_column='ALLOWED_DOWNTIME', blank=True, null=True)
    type = models.CharField(max_length=15, db_column='TYPE', blank=True, null=True)

    class Meta:
#        app_label = 'hosts'
        db_table = u'services'


