from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# from api.views.profile import UserProfileSerializer, UserSerializer
from api.models import Employee
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from knox.models import AuthToken
# from api.views.employee import EmployeeSerializer
from api.views.employee import AddressSerializer, EducationSerializer, DepartmentSerializer


# class CsrfExemptSessionAuthentication(SessionAuthentication):
#
#     def enforce_csrf(self, request):
#         return  # To not perform the csrf check previously happening
class NewJoineeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'first_name',
            'last_name',
            'profile_picture',
            'role',
            'joining_date',
            'nationality',
            # 'birth_date',

        )


class EmployeeSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)
    educations = EducationSerializer(many=True)
    department = DepartmentSerializer(many=False)
    new_employee = serializers.SerializerMethodField()

    def get_new_employee(self, employee):
        new_employee = Employee.objects.exclude(user=self.context.get("user")).order_by('-joining_date')[:10]
        new_employee_list = []
        for employee in new_employee:
            new_employee_list.append(NewJoineeSerializer(employee).data)
        return new_employee_list


        return NewJoineeSerializer(new_employee).data

    class Meta:
        model = Employee
        fields = '__all__'


class UserPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50)

    class Meta:
        model = Employee
        fields = ('email', 'password')


class LoginView(APIView):
    permission_classes = []
    serializer_class = UserPasswordSerializer

    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            raise serializers.ValidationError({"error": "Email required"})
        password = request.data.get('password')
        if not password:
            raise serializers.ValidationError({"error": "Password required"})
        if Employee.objects.filter(email=email).exists():
            username = Employee.objects.filter(email=email).first().user.username
            user = authenticate(username=username, password=password)
            if user:
                # stores = user.user_store_permissions.all()
                # store_list = []
                # for store in stores:
                #     store_list.append(StorePermissionSerializer(store).data)
                #
                # # token = Token.objects.get_or_create(user=user)
                token = AuthToken.objects.create(user)
                profile = EmployeeSerializer(user.profile, context={'request': request}).data
                return Response({
                    'token': token[1],
                    # 'user': profile,

                }, )

            return Response({'error': 'Wrong Password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": 'Employee not found'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        content = EmployeeSerializer(user.profile).data
        return Response(content)

    def get_serializer_context(self):
        context = super(ProfileView, self).get_serializer_context()
        context['user'] = self.request.user
        return context
