from rest_framework import serializers
from api.models import Employee, Address, Education, Department, Leave, KPI
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.utils import model_meta
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from zk import ZK, const


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'profile_picture')


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

    def get(self, request):
        conn = None
        zk = ZK('192.168.0.201', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        try:
            # connect to device
            conn = zk.connect()
            # disable device, this method ensures no activity on the device while the process is run
            conn.disable_device()
            # another commands will be here!
            # Example: Get All Users
            users = conn.get_users()
            for user in users:
                privilege = 'User'
                if user.privilege == const.USER_ADMIN:
                    privilege = 'Admin'
                print ('+ UID #{}'.format(user.uid))
                print ('  Name       : {}'.format(user.name))
                print ('  Privilege  : {}'.format(privilege))
                print ('  Password   : {}'.format(user.password))
                print ('  Group ID   : {}'.format(user.group_id))
                print ('  User  ID   : {}'.format(user.user_id))
            return Response({"connection": "Connected to ZKTecho and found data..."})
            # Test Voice: Say Thank You
            conn.test_voice()
            # re-enable device after all commands already executed
            conn.enable_device()
        except Exception as e:
            print ("Process terminate : {}".format(e))
        finally:
            if conn:
                conn.disconnect()
        return Response({"message": "KPI submit to manger"})

