from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)
    head_of_department = models.ForeignKey(User, on_delete=models.CASCADE, related_name='departments', null=True,
                                           blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    # as_process = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name
