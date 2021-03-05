import django_filters

import sef.user.models as models
from sef.common.filters import BaseFilterSet


class UserFilter(BaseFilterSet):

    class Meta:
        model = models.User
        fields = (
            'first_name', 'last_name', 'email',
            'phone_number',)


class UserProfileFilter(BaseFilterSet):

    class Meta:
        model = models.UserProfile
        fields = (
            'user__first_name', 'user__last_name', 'user__email',
            'user__phone_number',)
