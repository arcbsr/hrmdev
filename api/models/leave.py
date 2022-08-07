from django.db import models
from django.contrib.auth.models import User
from .profile import Employee

LEAVE_TYPE = (('annual', 'annual'),
              ('sick', 'sick'),
              ('others', 'others')
              )
STATUS = (('pending', 'pending'),
          ('approved', 'approved'))


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves', null=True,
                                 blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(choices=LEAVE_TYPE, default='annual', max_length=10)
    status = models.CharField(choices=STATUS, default='pending',max_length=20)
    total_day_count = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.employee.first_name
