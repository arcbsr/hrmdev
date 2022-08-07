from django.db import models
from django.contrib.auth.models import User
from .profile import Employee

STATUS = (('manager', 'manager'),
          ('ongoing', 'ongoing'),

          ('completed', 'completed')
          )


class KPI(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='kpis', null=True,
                                 blank=True)
    date = models.DateField()
    kpi_year = models.IntegerField()
    status = models.CharField(choices=STATUS, default='ongoing',max_length=20)
    goal = models.CharField(max_length=250)
    weightage = models.CharField(max_length=100)
    l2 = models.CharField(max_length=50,null=True,blank=True)
    l3 = models.CharField(max_length=50,null=True,blank=True)
    l4 = models.CharField(max_length=50,null=True,blank=True)
    l5 = models.CharField(max_length=50,null=True,blank=True)
    self_rating = models.CharField(max_length=50)
    comments = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.employee.first_name
