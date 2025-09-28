"""
Serializers for the user API view.
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers  # We need the way to convert objects to and from Python Objects, which is done by serializers.


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the user object. """

    class Meta:  # We tell DRF the additional arguments we want to pass to the serializer.
        model = get_user_model()  # We tell the serializer that this serializer is for the user model.
        fields = ['email', 'password', 'name']  # Needs to be created when you set a request. We don't set is_staff or things like that, because we don't want users to set that themselves.
        extra_kwargs = {
            'password': {'write_only': True,
                         'min_length': 5
                        }
        }

    def create(self, validated_data):
        """ Create and return a user with encrypted password. """
        return get_user_model().objects.create_user(**validated_data)