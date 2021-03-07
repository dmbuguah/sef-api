"""Facility serializers."""
from rest_framework import serializers

import sef.facility.models as models


class FacilitySerializer(serializers.ModelSerializer):
    """Facility serializer."""

    class Meta:
        """Facility serializer Meta class."""

        model = models.Facility
        fields = (
            'id', 'facility_name', 'facility_type', 'owner_name',
            'operation_status_name', 'latlong')


class FacilityLocationDetailSerializer(serializers.ModelSerializer):
    """Facility location serializer."""

    class Meta:
        """Facility location serializer Meta class."""

        model = models.FacilityLocationDetail
        fields = (
            'id', 'address', 'country', 'place', 'locality',
            'neighborhood', 'poi', 'landmark', 'postcode', 'district',
            'region')
