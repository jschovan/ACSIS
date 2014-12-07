from django.db import models
from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        compulsory_fields = ['service']
        fields = ('service', 'contacts', 'description', 'parents', 'doccard', \
        'criticality', 'allowed_downtime', 'type' ,)


    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(ServiceSerializer, self).__init__(*args, **kwargs)


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
        return Service(**validated_data)


