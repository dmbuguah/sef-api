"""Facility views."""
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from sef.facility import filters
from sef.facility import serializers
from sef.facility import models

from sef.common.views import SeFBaseViewSet
from sef.facility.analytics.analysis import (
    get_facilities, get_keph_levels, get_facility_owner,
    get_facility_type, search_facility)


class FacilityViewSet(SeFBaseViewSet):
    """This provides a way to add Facility details."""

    permission_classes = (AllowAny, )
    queryset = models.Facility.objects.all()
    filter_class = filters.FacilityFilter
    serializer_class = serializers.FacilitySerializer

    @list_route(methods=('get',))
    def facilities_near_me(self, request):
        """Get facilities near the user."""
        latitude = self.request.query_params['lat']
        longitude = self.request.query_params['lng']

        _response = get_facilities(latitude, longitude)

        keph_levels = get_keph_levels()
        facility_owner = get_facility_owner()
        facility_type = get_facility_type()

        _response['keph_levels'] = keph_levels
        _response['facility_owner'] = facility_owner
        _response['facility_type'] = facility_type

        return Response(_response)

    @list_route(methods=('get',))
    def search_facilities(self, request):
        """Search facilities."""
        lat = self.request.query_params['lat']
        lng = self.request.query_params['lng']
        facility_type = self.request.query_params['facility_type_value']
        keph_level = self.request.query_params['keph_level_value']
        facility_owner = self.request.query_params['facility_owner_value']
        radius = self.request.query_params['radius']

        response = search_facility(
            lat, lng, facility_type, keph_level, radius, facility_owner)

        return Response(response)


class FacilityLocationDetailViewSet(SeFBaseViewSet):
    """This provides a way to add Facility Location details."""

    permission_classes = (AllowAny, )
    queryset = models.FacilityLocationDetail.objects.all()
    filter_class = filters.FacilityLocationDetailFilter
    serializer_class = serializers.FacilityLocationDetailSerializer
