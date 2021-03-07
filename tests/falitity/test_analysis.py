import pytest

from django.contrib.gis.geos import Point

from model_mommy import mommy
from sef.facility.models import Facility

from django.test import TestCase
from sef.facility.analytics.analysis import (
    get_keph_levels, get_facility_owner, search_facility)


@pytest.mark.django_db
class TestAnalyticsModule(TestCase):
    def setUp(self):
        super(TestAnalyticsModule, self).setUp()

    def test_get_keph_levels(self):
        mommy.make(Facility, keph_level='Level 2', _quantity=4)
        mommy.make(Facility, keph_level='Level 7', _quantity=5)

        qualified_keph_level = get_keph_levels()
        assert len(qualified_keph_level) == 2

    def test_get_facility_owner(self):
        mommy.make(
            Facility, owner_name='Armed Forces', keph_level='Level 2',
            _quantity=4)
        mommy.make(
            Facility, owner_name='Ministry Of Health',
            keph_level='Level 2', _quantity=9)
        mommy.make(
            Facility, owner_name='Other Faith Based',
            keph_level='Level 2', _quantity=2)

        qualified_facility_owners = get_facility_owner()
        assert len(qualified_facility_owners) == 3

    def test_get_facility_type(self):
        mommy.make(
            Facility, facility_type='Dispensary', keph_level='Level 2',
            _quantity=9)
        mommy.make(
            Facility, owner_name='Medical Center',
            keph_level='Level 2', _quantity=2)

        qualified_facility_owners = get_facility_owner()
        assert len(qualified_facility_owners) == 2

    def test_search_facility(self):
        mommy.make(
            Facility, owner_name='Ministry Of Health',
            keph_level='Level 4', _quantity=4, facility_type='Dispensary',
            latlong=Point(float('36.7772037'), float('-1.2067487')))

        response = search_facility(
            '-1.2067487', '36.7772037', 'Dispensary', 'Level 4', 6,
            'Ministry Of Health')
        import pdb; pdb.set_trace()
        assert len(response['facility_location']['analysis_data']) == 4
