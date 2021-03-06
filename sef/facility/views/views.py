from sef.common.views import NuggetBaseViewSet
from sef.case import filters
from sef.case import serializers
from sef.case import models

from sef.facility.tasks.utils import geocode_reverse

from rest_framework.response import Response
from rest_framework.decorators import list_route


class FacilitySerializer(NuggetBaseViewSet):
    """
    This provides a way to add Case details.
    """
    permission_classes = (AllowAny, )
    queryset = models.Facility.objects.all()
    filter_class = filters.FacilityFilter
    serializer_class = serializers.FacilitySerializer


class FacilityLocationDetailViewSet(NuggetBaseViewSet):
    """
    This provides a way to add Case details.
    """
    permission_classes = (AllowAny, )
    queryset = models.CaseFile.objects.all()
    filter_class = filters.CaseFileFilter
    serializer_class = serializers.CaseFileSerializer


class LocationViewSet(NuggetBaseViewSet):
    """
    This provides a way to add Case details.
    """
    permission_classes = (AllowAny, )
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
