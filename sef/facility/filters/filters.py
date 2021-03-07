"""Facility filters."""
import django_filters

import sef.facility.models as models


class FacilityFilter(django_filters.FilterSet):
    """Facility filter class."""

    class Meta:
        """Facility meta class."""

        model = models.Facility
        fields = ('facility_name', 'facility_type')


class FacilityLocationDetailFilter(django_filters.FilterSet):
    """Facility location filter class."""

    class Meta:
        """Facility location meta class."""

        model = models.FacilityLocationDetail
        fields = ('place', 'locality',)
