from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# from .address import Address, Education
from .department import Department

# from django.contrib.auth.models import User
# from django.db import models
# from places.fields import PlacesField
# from django_google_maps import fields as map_fields
GENDER = ((
              'male', 'male'),
          ('female', 'female')
)
MARITAL_STATUS = (
    ('single', 'single'),
    ('married', 'married')

)

EMPLOYEE_TYPE = (('general', 'general'),
                 # ('manager', 'manager'),
                 ('hr', 'hr'))


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    id_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255,null=True)
    profile_picture = models.ImageField(
        null=True,
        blank=True
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees', null=True)
    manager = models.ForeignKey(User, related_name='employees', on_delete=models.SET_NULL, null=True,
                                blank=True)

    role = models.CharField(max_length=200, null=True)
    joining_date = models.DateField(null=True)
    company = models.CharField(max_length=255, null=True)
    total_leave = models.IntegerField(null=True, blank=True)
    remaining_leave = models.IntegerField(null=True, blank=True)
    profile_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPE, default='general')
    sex = models.CharField(max_length=20, choices=GENDER, default='male')
    nationality = models.CharField(max_length=100, null=True, blank=True)
    passport_or_nid = models.CharField(max_length=100, null=True)
    birth_date = models.DateField()

    # marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS, default='single')
    # address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='employees')
    phone = models.CharField(
        # help_text="eg: +8801*******, +88 is important",
        max_length=20,
        # blank=True,
        null=True,
        unique=True
    )
    emergency_phone = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True,unique=True)
    is_hr = models.BooleanField(default=False)
    # education = models.ForeignKey(Education, related_name='employees', on_delete=models.CASCADE, null=True)

    # profile_picture = models.ImageField(
    #     null=True,
    #     blank=True
    # )
    # fb_link = models.URLField(blank=True, null=True)
    # twitter_link = models.URLField(blank=True, null=True)
    # linked_in_link = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.first_name
