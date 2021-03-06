import django_filters

import sef.facility.models as models
from sef.common.filters import BaseFilterSet


class FacilityFilter(BaseFilterSet):

    class Meta:
        model = models.Facility
        fields = ('facility_name', 'facility_type')


class FacilityLocationDetailFilter(BaseFilterSet):

    class Meta:
        model = models.FacilityLocationDetail
        fields = ('place', 'locality',)
