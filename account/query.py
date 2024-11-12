import graphene
from django.db.models import Q
from account.models import *
from account.types import *
from account.pagination import *


class DesignationQuery(graphene.ObjectType):
    all_designations = graphene.Field(
        create_connection(DesignationType),  # Use create_connection directly
        search=graphene.String(),
        first=graphene.Int(),
        after=graphene.String(),
        last=graphene.Int(),
        before=graphene.String(),
        ordering=graphene.String()
    )
    designation = graphene.Field(
        DesignationType, 
        id=graphene.ID(required=True)
    )

    def resolve_all_designations(self, info, search=None, ordering="id", **kwargs):
        queryset = DesignationModel.objects.all()

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
            )

        return paginate_queryset(
            queryset=queryset,
            ordering_field=ordering,
            **kwargs
        )

    def resolve_designation(self, info, id):
        return DesignationModel.objects.get(pk=id)


class EmployeeQuery(graphene.ObjectType):
    all_employees = graphene.List(EmployeeType)
    
    def resolve_all_employees(self, info):
        return EmployeeModel.objects.all()




