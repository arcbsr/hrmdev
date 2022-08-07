from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser, FormParser
import json
from rest_framework import parsers
# import phonenumbers
import re
from rest_framework import serializers
# from phonenumbers.phonenumberutil import region_code_for_country_code
from django.utils import timezone
from datetime import timedelta
import random
# import requests
import urllib.parse
from django.contrib.auth.models import User


class MultiSerializerMixin(object):
    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        Thanks gonz: http://stackoverflow.com/a/22922156/11440

        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerMixin, self).get_serializer_class()