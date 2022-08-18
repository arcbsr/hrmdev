import json
from rest_framework import serializers
from api.models import Attendance, Employee , Department
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.utils import model_meta
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from datetime import datetime, date
from django.core.exceptions import ValidationError


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class EmployeeSerializer(serializers.ModelSerializer):

    department = DepartmentSerializer(many=False)
    class Meta:
        model = Employee
         
        fields = ('id', 'first_name', 'last_name', 'email', 'id_number', 'department')

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
        
        limit = int(request.GET.get('n')) or 20
        datee = request.GET.get('date') or ""
        try:
            if datee != datetime.strptime(datee, "%Y-%m-%d").strftime('%Y-%m-%d'):
                # return Response({ "error":"Incorrect data format, should be YYYY-MM-DD"})
                today = date.today()
                datee = today.strftime("%Y-%m-%d")
        except ValueError:
            # return Response({ "error":"Incorrect data format, should be YYYY-MM-DD"})
            today = date.today()
            datee = today.strftime("%Y-%m-%d")

        page = int(request.GET.get('page')) or 0
        offset = page * limit
        reports = []
        # for x in range(int(limit)):
        #     attn = Attendance()
        #     attn.employee = "Rajon" + str(x)
        #     attn.department = "Science"
        #     attn.intime = "10:12"
        #     attn.outtime = "10:12"

        empl = Employee.objects.all()[offset:offset+limit];
        for emp in empl:
            # reports.append(EmployeeSerializer(emp).data)
            atndnc = Attendance.objects.filter(lastdate__icontains = datee,employee_id = emp.id )[offset:offset+limit];
            datafound= False;
            innerValue = {}
            innerValue.update({"employee" : emp.first_name + " " + emp.last_name })
            innerValue.update({"department" : emp.department.name})
            if len(atndnc) > 0:
                datafound = True
            intime = ""
            for atn in atndnc:
                # data = AttendanceSerializer(atn)
                if atn.intime and len(intime) == 0:
                    innerValue.update({"intime" : atn.intime})
                if atn.outtime:
                    innerValue.update({"outtime" : atn.outtime})
                innerValue.update({"terminal_sn" : atn.terminal_sn})
                innerValue.update({"terminal_name" : atn.terminal_name})
            
            if datafound:
                reports.append(innerValue)

        return Response({ "count": len(reports), "reports": reports})

