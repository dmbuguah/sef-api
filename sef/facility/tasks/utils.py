"""Reverse Geocode Module."""
from sef.constants import (HEADERS, KMFL_URL, KMFL_FACILITY_URL)
from sef.facility.utils import create_session

from sef.case.models import Location, LocationDetails

from mapbox import Geocoder
from progress.bar import Bar

def get_kmfl_falicities():
    s, session_response = create_session()

    if session_response.status_code = 200:
        facility_url = KMFL_URL + KMFL_FACILITY_URL
        response = s.get(url=facility_url, headers=HEADERS)

        if response.status_code == 200:
            return getResponse.json()


def process_facility_data():
    facility_data = get_kmfl_falicities()
