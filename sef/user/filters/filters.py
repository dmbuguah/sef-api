import django_filters

import sef.user.models as models
from sef.common.filters import BaseFilterSet


class UserFilter(BaseFilterSet):

    class Meta:
        model = models.User
        fields = (
            'first_name', 'last_name', 'email',
            'phone_number',)
