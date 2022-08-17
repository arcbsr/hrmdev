from rest_framework import serializers
from api.models import Employee, Address, Education, Department, Leave, KPI
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.utils import model_meta
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from zk import ZK, const
from ..models.attendance import Attendance
from django.forms.models import model_to_dict
from api.views import employee
import json

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'email', 'id_number')


class RequestedKPISerializer(serializers.ModelSerializer):
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
        model = KPI
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


class KPISerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        kpi = KPI(**validated_data)
        kpi.employee = self.context.get("employee")
        kpi.clean()
        kpi.save()
        return kpi

    class Meta:
        model = KPI
        fields = "__all__"


class KPIViewSet(
    # MultiSerializerMixin,
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = KPISerializer

    # parser_classes = (JSONParser, MultipartJsonParser)

    def get_serializer_context(self):
        context = super(KPIViewSet, self).get_serializer_context()
        context['employee'] = self.request.user.profile
        return context

    def get_queryset(self):
        qs = KPI.objects.filter(employee=self.request.user.profile, status='ongoing')
        return qs


class RequestedKPIViewSet(
    # MultiSerializerMixin,
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = RequestedKPISerializer

    # parser_classes = (JSONParser, MultipartJsonParser)

    # def get_serializer_context(self):
    #     context = super(KPIViewSet, self).get_serializer_context()
    #     context['employee'] = self.request.user.profile
    #     return context

    def get_queryset(self):
        qs = KPI.objects.filter(employee__manager=self.request.user.id, status='manager')
        return qs


class SubmitKPIView(APIView):
    # permission_classes = []
    # serializer_class = UserPasswordSerializer

    # authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self, request):
        request.user.profile.kpis.filter(status='ongoing').update(status='manager')
        return Response({"message": "KPI submit to manger"})



class GetDataZK(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        # print(request.data)
        emp = Employee.objects.all()
        new_employee_list = []
        # for employee in emp:
        #     new_employee_list.append(EmployeeSerializer(employee).data)
        atn= AttendanceSerializer(Attendance.objects.all().last()) .data
        return Response({"message": {"lastsaved": atn['lastdate'] or "", "emp": new_employee_list}})


    def get(self, request): 
        
        try:
            
            return Response({"connection": "Connected to ZKTecho and found data..."})
            # Test Voice: Say Thank You
            conn.test_voice()
            # re-enable device after all commands already executed
            conn.enable_device()
        except Exception as e:
            print ("Process terminate : {}".format(e))
        
        return Response({"message": "KPI submit to manger"})

class AddAttendanceFromZK(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request, format=None):
        jtopy=json.dumps(request.data)
        dict_json=json.loads(jtopy)
        ds = []
        for val in dict_json['data']:
            print(val['emp_code'])
            emp_id = val['emp_code'] 
            emp = Employee.objects.filter(id_number = emp_id).order_by('id').first()
            atnd = Attendance ()
            atnd.employee = emp
            atnd.terminal_sn = val['terminal_sn']
            atnd.terminal_name = val['terminal_alias']
            if val['punch_state'] == "0":
                atnd.intime = val['punch_time']
                atnd.lastdate = val['punch_time']


            elif val['punch_state'] == "1":
                atnd.outtime = val['punch_time']
                atnd.lastdate = val['punch_time']


            ds.append(AttendanceSerializer(atnd).data)
            atnd.save()

        return Response({"message":  "success"})

class EmployeeSerializerInShort(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'email', 'id_number')
class AttendanceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializerInShort(read_only=True)

    class Meta:
        model = Attendance
        extra_kwargs = { 
            'intime': {'required': False},
            'outtime': {'required': False},
            'lastdate': {'required': False} 
        }
        fields = "__all__"
