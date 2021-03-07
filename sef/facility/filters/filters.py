import django_filters

import sef.facility.models as models


class FacilityFilter(django_filters.FilterSet):

    class Meta:
        model = models.Facility
        fields = ('facility_name', 'facility_type')


class FacilityLocationDetailFilter(django_filters.FilterSet):

    class Meta:
        model = models.FacilityLocationDetail
        fields = ('place', 'locality',)
