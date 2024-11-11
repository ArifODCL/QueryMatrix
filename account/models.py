from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class DesignationModel(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class UserModel(AbstractUser):
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class EmployeeModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="employee_user")
    designation = models.ForeignKey(DesignationModel, on_delete=models.CASCADE, related_name="employee_designation")
    date_of_join = models.DateField(null=True)

    def __str__(self):
        return f"E{self.id}-{self.user.get_full_name()}"


    




