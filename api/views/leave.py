from rest_framework import serializers
from api.models import Employee, Address, Education, Department, Leave
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.utils import model_meta


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'profile_picture')


class RequestedLeaveSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        instance.save()

        return instance

    class Meta:
        model = Leave
        extra_kwargs = {
            'start_date': {'required': False},
            'end_date': {'required': False},
            'comment': {'required': False},
        }
        fields = '__all__'


class LeaveSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        #
        leave = Leave(**validated_data)
        leave.employee = self.context.get("employee")
        leave.clean()
        leave.save()
        return leave

    class Meta:
        model = Leave
        fields = "__all__"


class LeaveViewSet(
    # MultiSerializerMixin,
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = LeaveSerializer

    # parser_classes = (JSONParser, MultipartJsonParser)

    def get_serializer_context(self):
        context = super(LeaveViewSet, self).get_serializer_context()
        context['employee'] = self.request.user.profile
        return context

    def get_queryset(self):
        qs = Leave.objects.filter(employee=self.request.user.profile, status='pending')
        return qs


class RequestedLeaveViewSet(
    # MultiSerializerMixin,
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = RequestedLeaveSerializer

    # parser_classes = (JSONParser, MultipartJsonParser)

    # def get_serializer_context(self):
    #     context = super(LeaveViewSet, self).get_serializer_context()
    #     context['employee'] = self.request.user.profile
    #     return context

    def get_queryset(self):
        qs = Leave.objects.filter(employee__manager=self.request.user, status='pending')
        return qs
