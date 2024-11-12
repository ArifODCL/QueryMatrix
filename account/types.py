from graphene_django import DjangoObjectType
from account.models import *

class DesignationType(DjangoObjectType):
    class Meta:
        model = DesignationModel
        name = "DesignationModel"
        fields = "__all__"


class EmployeeType(DjangoObjectType):
    class Meta:
        model = EmployeeModel
        name = "EmployeeModel"
        fields = "__all__"
