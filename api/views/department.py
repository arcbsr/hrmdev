from rest_framework import serializers
from api.models import Employee, Address, Education, Department
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from api.views.utils import MultiSerializerMixin
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import uuid
from rest_framework import generics


#


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DepartmentViewSet(
    # MultiSerializerMixin,
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = DepartmentSerializer

    # parser_classes = (JSONParser, MultipartJsonParser)

    def get_queryset(self):
        qs = Department.objects.all()
        return qs




