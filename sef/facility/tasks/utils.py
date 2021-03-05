"""Reverse Geocode Module."""
from sef.case.models import Location, LocationDetails

from mapbox import Geocoder
from progress.bar import Bar

def geocode_reverse(reverse_file=None, case=None):
    location = Location.objects.filter(case_id=case.id)
    all_loc = location.count()
    bar = Bar('Processing', max=all_loc)

    i = 0
    for loc in location:
        i += 1
        latlong = loc.latlong.coords
        geocoder = Geocoder()

        response = geocoder.reverse(lon=latlong[0], lat=latlong[1])
        features = sorted(
            response.geojson()['features'], key=lambda x: x['place_name'])

        if features:
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

            location_data = {
                'location': loc,
                'address': address,
                'postcode': postcode,
                'place': place,
                'neighborhood': neighborhood,
                'country': country,
                'region': region,
            }
        else:
            location_data = {
                'location': loc,
                'address': 'N/A',
                'postcode': 'N/A',
                'place': 'N/A',
                'neighborhood': 'N/A',
                'country': 'N/A',
                'region': 'N/A',
            }
        bar.next()
        print('Progress: Decoding-----{}/{}'.format(i, all_loc))
        LocationDetails.objects.create(**location_data)
    bar.finish()
