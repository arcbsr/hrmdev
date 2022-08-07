from django.contrib import admin
from .models import Address, Department, Employee, Education, KPI, Leave

# Register your models here.
admin.site.register(Address)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Education)
admin.site.register(KPI)
admin.site.register(Leave)
