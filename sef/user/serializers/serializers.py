"""User Serializers."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

import sef.user.models as models


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    full_name = serializers.ReadOnlyField()
    image_obj_id = serializers.ReadOnlyField(source='user_profile.id')

    class Meta:
        """User serializer meta class."""

        model = models.User
        fields = (
            'id', 'first_name', 'last_name', 'id', 'email', 'full_name',
            'is_active', 'password', 'image', 'phone_number', 'is_admin',
            'image_obj_id')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }
        read_only_fields = ('last_login', )

    def create(self, validated_data):
        """Overide user create method."""
        return get_user_model().objects.create_user(**validated_data)
