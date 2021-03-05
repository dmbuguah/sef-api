import django_filters

import sef.case.models as models
from sef.common.filters import BaseFilterSet


class CaseFilter(BaseFilterSet):

    class Meta:
        model = models.Case
        fields = ('title', 'description')


class CaseFileFilter(BaseFilterSet):

    class Meta:
        model = models.CaseFile
        fields = ('platform', 'file_path',)


class LocationeFilter(BaseFilterSet):

    class Meta:
        model = models.Location
        fields = (
            'case', 'source',
            'confidence', 'timestamp')
