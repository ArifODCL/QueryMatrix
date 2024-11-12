import graphene
from graphene_django import DjangoObjectType
from account.models import *


class DesignationType(DjangoObjectType):
    class Meta:
        model = DesignationModel
        fields = "__all__"


class EmployeeType(DjangoObjectType):
    class Meta:
        model = EmployeeModel
        fields = "__all__"


class Query(graphene.ObjectType):
    all_designations = graphene.List(DesignationType)
    all_employees = graphene.List(EmployeeType)

    def resolve_all_designations(self, info):
        return DesignationModel.objects.all()

    def resolve_all_employees(self, info):
        return EmployeeModel.objects.all()

schema = graphene.Schema(query=Query)



