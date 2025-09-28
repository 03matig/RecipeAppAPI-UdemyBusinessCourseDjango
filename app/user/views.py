"""
Views for the user API.
"""

# We handle logic for creating objects in the database, by providing a bunch of different base classes we can configure for our views that will handle the request.
# At the same time, gives us the ability to override some of that behavior so we can modify it if we need.
from rest_framework import generics

from user.serializers import UserSerializer  # This is the serializer we created on the serializers.py file.


class CreateUserView(generics.CreateAPIView):  # This method handles an HTTP request designed for creating objects.
    """ Create a new user in the system. """
    serializer_class = UserSerializer  # All you need to do is define and set the serializer class and view so DRF knows what serialize we want to use.