from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
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
from api.views.employee import EmployeeSerializer
from django.conf import settings


class ForgotPasswordSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=50)

    class Meta:
        model = Employee
        fields = ('email',)


class ForgotPasswordView(APIView):
    permission_classes = []
    serializer_class = ForgotPasswordSerializer

    # authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            raise serializers.ValidationError({"error": "Email required"})

        if Employee.objects.filter(email=email).exists():
            user = Employee.objects.filter(email=email).first().user
            # user = authenticate(username=username, password=password)
            if user:
                subject = "Forgot Password Requested"
                password = User.objects.make_random_password()
                user.set_password(password)
                # user.save()  need to back when email server is ok.
                body = "your password is {}".format(password)
                from_email = settings.EMAIL_HOST_USER
                # send_mail(subject, body, from_email, [email,])

                return Response({
                    'message': "Sent password to your mail",
                    # 'user': profile,

                }, )

        return Response({"error": 'Employee not found'}, status=status.HTTP_400_BAD_REQUEST)
