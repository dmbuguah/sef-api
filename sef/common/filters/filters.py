import django_filters

from sef.pg_search.filters import SearchFilter


class BaseFilterSet(django_filters.FilterSet):
    search = SearchFilter()
