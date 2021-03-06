"""Reverse Geocode Module."""
from mapbox import Geocoder

from sef.facility.models import Facility, FacilityLocationDetail


def geocode_reverse():
    facilities = Facility.objects.filter(latlong__isnull=False)
    import pdb; pdb.set_trace()
    for fac in facilities:
        latlong = fac.latlong.coords
        geocoder = Geocoder()

        response = geocoder.reverse(lon=latlong[0], lat=latlong[1])
        features = sorted(
            response.geojson()['features'], key=lambda x: x['place_name'])

        if features:
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
        else:
            facility_location_detail = {
                'facility': fac,
                'address': 'N/A',
                'postcode': 'N/A',
                'place': 'N/A',
                'neighborhood': 'N/A',
                'country': 'N/A',
                'region': 'N/A',
            }
        FacilityLocationDetail.objects.create(**facility_location_detail)
