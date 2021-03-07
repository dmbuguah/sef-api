"""User filters."""
import django_filters

import sef.user.models as models


class UserFilter(django_filters.FilterSet):
    """User filter class."""

    class Meta:
        """User meta class."""

        model = models.User
        fields = (
            'first_name', 'last_name', 'email',
            'phone_number',)
