from rest_framework import serializers
from api.models import Employee, Address, Education, Department
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from api.views.utils import MultiSerializerMixin
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import uuid
from rest_framework import generics
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser, FormParser
from rest_framework import parsers
import json
from rest_framework.response import Response

class MultipartJsonParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        data = {}

        for key, value in result.data.items():
            if type(value) != str:
                data[key] = value
                continue
            if '{' in value or "[" in value:
                try:
                    data[key] = json.loads(value)
                except ValueError:
                    data[key] = value
            else:
                data[key] = value

        return parsers.DataAndFiles(data, result.files.dict())


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('employee',)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class EducationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ('employee',)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(required=True, write_only=True)
    addresses = AddressCreateSerializer(many=True)
    educations = EducationCreateSerializer(many=True)

    # @staticmethod
    # def update_adresses(instance, addresses_data):
    #     address_id = []
    #     for address in addresses_data:
    #         product = purchase_item.get('product', None)
    #         quantity = purchase_item.get('quantity', None)
    #         price = purchase_item.get('price', None)
    #         unit = purchase_item.get('unit', None)
    #         if not product:
    #             product_name = purchase_item.get('product_name', None)
    #             if not product_name:
    #                 raise serializers.ValidationError({"product_name": "Product name should not empty"})
    #
    #             product, created = Product.objects.get_or_create(name=product_name, store=store)
    #             product.unit_price = price
    #             product.unit = unit
    #             product.save()
    #         if PurchaseItem.objects.filter(purchase=instance, product=product).exists():
    #             purchase_item_instance = PurchaseItem.objects.filter(purchase=instance, product=product).first()
    #             purchase_item_instance.unit = unit
    #             purchase_item_instance.quantity = quantity
    #             purchase_item_instance.price = price
    #             purchase_item_instance.save()
    #             purchase_item_id.append(purchase_item_instance.id)
    #         else:
    #             purchase_item_instance = PurchaseItem(purchase=instance, product=product, quantity=quantity,
    #                                                   price=price, unit=unit)
    #             try:
    #                 purchase_item_instance.clean()
    #                 purchase_item_instance.save()
    #                 purchase_item_id.append(purchase_item_instance.id)
    #             except ValidationError as e:
    #                 raise serializers.ValidationError({"error": [e.message]})
    #     instance.purchase_items.exclude(id__in=purchase_item_id).delete()

    def create(self, validated_data):
        addresses_data = []
        educations_data = []
        if 'addresses' in validated_data:
            addresses_data = validated_data.pop('addresses')
        if 'educations' in validated_data:
            educations_data = validated_data.pop('educations')

        # password = validated_data.pop('password')
        password = '12345'

        user = User.objects.create_user(
            username=str(uuid.uuid4()),
            password=password
        )
        try:
            employee = Employee(user=user, **validated_data)
            employee.clean()
            employee.save()
        except Exception as e:
            raise serializers.ValidationError({"error": [e.message]})
        for address_data in addresses_data:
            address_instance = Address(employee=employee, **address_data)
            try:
                address_instance.clean()
                address_instance.save()
            except ValidationError as e:
                raise serializers.ValidationError({"error": [e.message]})
        for education_data in educations_data:
            education_instance = Education(employee=employee, **education_data)
            try:
                education_instance.clean()
                education_instance.save()
            except ValidationError as e:
                raise serializers.ValidationError({"error": [e.message]})
        return employee

    # def update(self, instance, validated_data):
    #     # store = Store.objects.get(id=int(self.context.get("store_id")))
    #
    #     if 'addresses' in validated_data:
    #         addresses_data = validated_data.pop('addresses')
    #         self.update_purchase_items(instance, purchase_items_data, store)
    #     purchase = self.update_purchase(instance, validated_data, store, user=self.context.get('user'))
    #     if purchase.mine and purchase.vice_versa:
    #         purchase_vice_versa(purchase, updated=True)
    #     return purchase

    class Meta:
        model = Employee
        exclude = ('user',)


class EmployeeSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)
    educations = EducationSerializer(many=True)
    department = DepartmentSerializer(many=False)

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeViewSet(
    MultiSerializerMixin,
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = EmployeeSerializer

    parser_classes = (JSONParser, MultipartJsonParser)

    def get_queryset(self):
        qs = Employee.objects.all()
        return qs 
        # user = self.request.user
        # store = self.request.META.get('HTTP_STORE_ID', None)
        # if user.user_store_permissions.filter(store=store).exists():
        #     if user.user_store_permissions.filter(store=store).first().purchase_permission:
        #         qs = Purchase.objects.filter(store=store)
        #         return qs
        #
        # return []
    
    # def get_serializer_context(self):
    #     context = super(EViewSet, self).get_serializer_context()
    #     context['store_id'] = self.request.META.get('HTTP_STORE_ID', None)
    #     context['user'] = self.request.user
    #     return context

    serializer_action_classes = {
        'list': EmployeeSerializer,
        'retrieve': EmployeeSerializer,
        'create': EmployeeCreateUpdateSerializer,
        'update': EmployeeSerializer,
    }


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id','user_id',
                  'first_name',
                  'last_name')


class ManagerView(generics.ListAPIView):
    serializer_class = ManagerSerializer

    def get_queryset(self):
        return Employee.objects.all()

