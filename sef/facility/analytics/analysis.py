"""Analysis module."""
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance

from sef.facility import models


def compose_payload(facilities):
    """Compose facility payload."""
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

    response = {
        'facility_location': {
            'title': 'Search For Facility Near You',
            'analysis_data': qualified_facilities
        },
    }

    return response


def get_facilities(latitude, longitude):
    """Given the latitude and longitude, return facilities."""
    point = Point(float(longitude), float(latitude))

    facilities = models.Facility.objects.filter(
        latlong__distance_lt=(point, Distance(km=2))).values(
            'id', 'facility_name', 'latlong', 'facility_type',
            'owner_name', 'operation_status_name', 'keph_level',
            'county_name')

    response = compose_payload(facilities)

    return response


def get_keph_levels():
    """Get all distinct kph levels."""
    keph_level = models.Facility.objects.filter(
        keph_level__isnull=False).values(
        'keph_level').order_by('keph_level').distinct('keph_level')

    qualified_keph_level = [
        {
            'name': q['keph_level'],
            'id': i
        } for i, q in enumerate(keph_level)]
    return qualified_keph_level


def get_facility_owner():
    """Get all distinct facility owners."""
    facility_owner = models.Facility.objects.filter(
        keph_level__isnull=False).values(
        'owner_name').order_by(
        'owner_name').distinct('owner_name')

    qualified_facility_owner = [
        {
            'name': q['owner_name'],
            'id': i
        } for i, q in enumerate(facility_owner)]
    return qualified_facility_owner


def get_facility_type():
    """Get all distinct facility owners."""
    facility_owner = models.Facility.objects.filter(
        keph_level__isnull=False).values(
        'facility_type').order_by(
        'facility_type').distinct('facility_type')

    qualified_facility_type = [
        {
            'name': q['facility_type'],
            'id': i
        } for i, q in enumerate(facility_owner)]
    return qualified_facility_type


def search_facility(
        lat, lng, facility_type, keph_level, radius, facility_owner):
    """Search Faciities given search parameter."""
    point = Point(float(lng), float(lat))
    facilities = models.Facility.objects.filter(
        latlong__distance_lt=(point, Distance(km=radius)),
        facility_type=facility_type,
        keph_level=keph_level,
        owner_name=facility_owner).values(
            'id', 'facility_name', 'latlong', 'facility_type',
            'owner_name', 'operation_status_name', 'keph_level',
            'county_name')

    response = compose_payload(facilities)

    return response
