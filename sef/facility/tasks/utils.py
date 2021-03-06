"""Reverse Geocode Module."""
from sef.constants import (HEADERS, KMFL_URL, KMFL_FACILITY_URL)
from sef.facility.utils import CreateSession

from sef.facility.models import Facility

from mapbox import Geocoder
from progress.bar import Bar

from django.contrib.gis.geos import fromstr


def get_kmfl_falicities(next_url=None):
    cs = CreateSession()
    cs.create_session()

    if cs.session_response.status_code == 200:
        facility_url = KMFL_URL + KMFL_FACILITY_URL
        if next_url:
            facility_url = next_url
        response = cs.session.get(url=facility_url, headers=HEADERS)

        if response.status_code == 200:
            return response.json()


def process_facility_data(next_url=None):
    result_data = get_kmfl_falicities(next_url=next_url)
    results = result_data['results']

    if results:
        facility_data = []

        for r in results:
            l_l = r['lat_long']
            latlong = fromstr(
                f'POINT({float(l_l[1])} {float(l_l[0])})', srid=4326) if \
                    l_l else None

            fd = {
                'facility_id': r['id'],
                'facility_name': r['name'],
                'facility_type': r['facility_type_name'],
                'owner_name': r['owner_name'],
                'latlong': latlong,
                'keph_level': r['keph_level_name'],
                'operation_status_name': r['operation_status_name'],
                'county_name': r['county_name'],
                'constituency_name': r['constituency_name'],
                'county_name': r['county_name'],
            }
            facility_data.append(fd)

        if facility_data:
            Facility.objects.bulk_create(
                    [ Facility(**f) for f in facility_data ])

    has_next = result_data['next']
    while has_next:
        process_facility_data(next_url=has_next)

def geocode_reverse():
    pass
