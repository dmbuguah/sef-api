import os

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet

class SelectSerializerMixin:
    """
    Allows the view to work with two serializers : one for reading data
    and another for writing data.

    It gives the view the `_read_serializer_class` if the request is a write
    request (post, put, patch), otherwise the `_read_serializer_class`.

    If `_read_serializer_class` is not set and the method is write,
    it gives `serializer_class`.
    """
    _read_serializer_class = None
    _write_serializer_class = None

    def get_serializer_class(self):
        active_methods = ['POST', 'PUT', 'PATCH']
        passive_methods = ['GET', 'OPTIONS', 'HEAD']

        method = self.request.method

        if self._write_serializer_class and method in active_methods:
            return self._write_serializer_class

        elif self._read_serializer_class and method in passive_methods:
            return self._read_serializer_class

        else:
            return super().get_serializer_class()


class SeFBaseViewSet(SelectSerializerMixin, ModelViewSet):
    pass
