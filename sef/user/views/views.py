from rest_framework import generics, status, decorators
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist

from sef.common.views import NuggetBaseViewSet
import sef.user.filters as filters
import sef.user.serializers as serializers
import sef.user.models as models
from rest_framework.response import Response


class UserViewSet(NuggetBaseViewSet):
    """
    This is the user's endpoint. It contains the details that are stored for
    a user using our system.
    """
    permission_classes = (AllowAny, )
    queryset = models.User.objects.all()
    filter_class = filters.UserFilter
    serializer_class = serializers.UserSerializer
    search_fields = ('first_name', 'last_name', 'email')


class MeView(generics.RetrieveUpdateDestroyAPIView):
    """
    This view is user to get the details of a logged in user.
    """
    queryset = None
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user
