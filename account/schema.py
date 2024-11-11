import graphene
from graphene_django import DjangoObjectType
from account.models import *


class DesignationType(DjangoObjectType):
    class Meta:
        model = DesignationModel
        fields = "__all__"

class DesiognationQuery(graphene.ObjectType):
    all_designations = graphene.List(DesignationType)

    def resolve_all_designations(self, info):
        return DesignationModel.objects.all()

designation_schema = graphene.Schema(query=DesiognationQuery)

class EmployeeType(DjangoObjectType):
    class Meta:
        model = EmployeeModel
        fields = "__all__"


