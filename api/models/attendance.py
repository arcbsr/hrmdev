from django.db import models
from django.contrib.auth.models import User
from .profile import Employee
from .department import Department

class Attendance(models.Model):
    employee =  models.CharField(max_length=250)
    # models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance', null=True,
    #                              blank=True)
    department = models.CharField(max_length=250)
    # models.ForeignKey(Department, on_delete=models.CASCADE, related_name='attendance', null=True,
    #                              blank=True)  
    intime = models.CharField(max_length=250)
    outtime = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.employee.first_name
