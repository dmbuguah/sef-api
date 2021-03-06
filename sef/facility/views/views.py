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
            'facility_location': {
                'title': 'Search For Facility Near You',
                'analysis_data': qualified_facilities
            },
        }

        return _response


    def get_keph_levels(self):
        keph_level = models.Facility.objects.filter(
            keph_level__isnull=False).values(
            'keph_level').order_by('keph_level').distinct('keph_level')

        qualified_keph_level = [
            {
                'name': q['keph_level'],
                'id': i
            } for i,q in enumerate(keph_level)]
        return qualified_keph_level


    def get_facility_owner(self):
        facility_owner = models.Facility.objects.filter(
            keph_level__isnull=False).values(
            'owner_name').order_by(
            'owner_name').distinct('owner_name')

        qualified_facility_owner = [
            {
                'name': q['owner_name'],
                'id': i
            } for i,q in enumerate(facility_owner)]
        return qualified_facility_owner


    def get_facility_type(self):
        facility_owner = models.Facility.objects.filter(
            keph_level__isnull=False).values(
            'facility_type').order_by(
            'facility_type').distinct('facility_type')

        qualified_facility_type = [
            {
                'name': q['facility_type'],
                'id': i
            } for i,q in enumerate(facility_owner)]
        return qualified_facility_type


    @list_route(methods=('get',))
    def facilities_near_me(self, request):
        latitude = self.request.query_params['lat']
        longitude = self.request.query_params['lng']

        _response = self.get_facilities(latitude, longitude)

        keph_levels = self.get_keph_levels()
        facility_owner = self.get_facility_owner()
        facility_type = self.get_facility_type()

        _response['keph_levels'] = keph_levels
        _response['facility_owner'] = facility_owner
        _response['facility_type'] = facility_type

        return Response(_response)

class FacilityLocationDetailViewSet(NuggetBaseViewSet):
    """
    This provides a way to add Facility Location details.
    """
    permission_classes = (AllowAny, )
    queryset = models.FacilityLocationDetail.objects.all()
    filter_class = filters.FacilityLocationDetailFilter
    serializer_class = serializers.FacilityLocationDetailSerializer
