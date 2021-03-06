from sef.common.views import NuggetBaseViewSet
from sef.facility import filters
from sef.facility import serializers
from sef.facility import models

from sef.facility.tasks.utils import geocode_reverse

from rest_framework.response import Response
from rest_framework.decorators import list_route


class FacilityViewSet(NuggetBaseViewSet):
    """
    This provides a way to add Facility details.
    """
    permission_classes = (AllowAny, )
    queryset = models.Facility.objects.all()
    filter_class = filters.FacilityFilter
    serializer_class = serializers.FacilitySerializer


class FacilityLocationDetailViewSet(NuggetBaseViewSet):
    """
    This provides a way to add Facility Location details.
    """
    permission_classes = (AllowAny, )
    queryset = models.FacilityLocationDetail.objects.all()
    filter_class = filters.FacilityLocationDetailFilter
    serializer_class = serializers.FacilityLocationDetailFileSerializer
