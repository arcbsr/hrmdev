import json
from rest_framework import serializers
from api.models import Attendance, Employee
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.utils import model_meta
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'email', 'id_number')

class AttendanceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    class Meta:
        model = Attendance
        fields = "__all__"


class RequestedKPISerializer(serializers.ModelSerializer):
    attendance = AttendanceSerializer(read_only=True)
 
    class Meta:
        model = Attendance
        extra_kwargs = {
            'employee': {'required': False},
            'comments': {'required': False},
            'self_rating': {'required': False},
            'weightage': {'required': False},
            'date': {'required': False},
            'kpi_year': {'required': False},
            'goal': {'required': False}
        }
        fields = "__all__"


class AttendanceSerializer2(serializers.ModelSerializer):
    def create(self, validated_data):
        kpi = Attendance(**validated_data)
        kpi.employee = self.context.get("employee")
        kpi.clean()
        kpi.save()
        return kpi

    class Meta:
        model = Attendance
        fields = "__all__"


class AttendanceViewSet(
    # MultiSerializerMixin,
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = AttendanceSerializer

    # parser_classes = (JSONParser, MultipartJsonParser)
    
class GetRepotFP(APIView):
    
    # ?date=12-10-2022&dept=science&emp=name
    permission_classes = []
    authentication_classes = []
    def get(self, request):
        
        limit = request.GET.get('n') or 50
        reports = []
        atndnc = Attendance.objects.all();
        # for x in range(int(limit)):
        #     attn = Attendance()
        #     attn.employee = "Rajon" + str(x)
        #     attn.department = "Science"
        #     attn.intime = "10:12"
        #     attn.outtime = "10:12"
        for atn in atndnc:
            reports.append(AttendanceSerializer(atn).data)
        
        
        return Response({"reports": atn})

