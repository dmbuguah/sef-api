from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance

from rest_framework.decorators import list_route
from rest_framework.response import Response
from sef.common.views import NuggetBaseViewSet
from sef.facility import filters
from sef.facility import serializers
from sef.facility import models

from sef.facility.tasks.utils import geocode_reverse

from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny


class FacilityViewSet(NuggetBaseViewSet):
    """
    This provides a way to add Facility details.
    """
    permission_classes = (AllowAny, )
    queryset = models.Facility.objects.all()
    filter_class = filters.FacilityFilter
    serializer_class = serializers.FacilitySerializer

    def get_facilities(self, latitude, longitude):
        point = Point(float(longitude), float(latitude))
        facilities = models.Facility.objects.filter(
            latlong__distance_lt=(point, Distance(km=2))).values(
                'id', 'facility_name', 'latlong', 'facility_type', 'owner_name',
                'operation_status_name', 'keph_level', 'county_name')

        qualified_facilities = [
            {
                'id': q['id'],
                'lat': q['latlong'].coords[1],
                'lng': q['latlong'].coords[0],
                'facility_name': q['facility_name'],
                'facility_type': q['facility_type'],
                'owner_name': q['owner_name'],
                'operation_status_name': q['operation_status_name'],
                'keph_level': q['keph_level'],
                'county_name': q['county_name']
            } for q in facilities]

        _response = {
            'location_case': {
                'title': 'Facility location data',
                'analysis_data': qualified_facilities
            },
        }

        return qualified_facilities

    @list_route(methods=('get',))
    def facilities_near_me(self, request):
        latitude = self.request.query_params['lat']
        longitude = self.request.query_params['lng']

        _response = self.get_facilities(latitude, longitude)
        return Response(_response)

class FacilityLocationDetailViewSet(NuggetBaseViewSet):
    """
    This provides a way to add Facility Location details.
    """
    permission_classes = (AllowAny, )
    queryset = models.FacilityLocationDetail.objects.all()
    filter_class = filters.FacilityLocationDetailFilter
    serializer_class = serializers.FacilityLocationDetailSerializer
