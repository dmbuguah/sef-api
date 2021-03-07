import django_filters

import sef.user.models as models

class UserFilter(django_filters.FilterSet):

    class Meta:
        model = models.User
        fields = (
            'first_name', 'last_name', 'email',
            'phone_number',)
