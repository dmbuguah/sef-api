"""Reverse Geocode Module."""
from mapbox import Geocoder

from sef.facility.models import Facility, FacilityLocationDetail


def create_faility(fac, features):
    """Create facility funtion."""
    address = postcode = place = neighborhood = country = region = None
    for f in features:
        if f['place_type'][0] == 'address':
            address = f['place_name']

        if f['place_type'][0] == 'postcode':
            postcode = f['place_name']

        if f['place_type'][0] == 'place':
            place = f['place_name']

        if f['place_type'][0] == 'neighborhood':
            neighborhood = f['place_name']

        if f['place_type'][0] == 'country':
            country = f['place_name']

        if f['place_type'][0] == 'region':
            region = f['place_name']

    facility_location_detail = {
        'facility': fac,
        'address': address,
        'postcode': postcode,
        'place': place,
        'neighborhood': neighborhood,
        'country': country,
        'region': region,
    }
    FacilityLocationDetail.objects.create(**facility_location_detail)


def geocode_reverse():
    """Reverse geocode coordinates."""
    facilities = Facility.objects.filter(latlong__isnull=False)
    for fac in facilities:
        latlong = fac.latlong.coords
        geocoder = Geocoder()

        response = geocoder.reverse(lon=latlong[0], lat=latlong[1])
        features = sorted(
            response.geojson()['features'], key=lambda x: x['place_name'])

        create_faility(fac, features)
